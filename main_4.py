import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import re


async def update_plot(api, ax, ydata, line, value_text, interval):
    while True:
        telegram = await api.telegram()
        import_kw, export_kw = parse_telegram_power(telegram)
        household_consumption_kw = import_kw + export_kw
        household_consumption_w = household_consumption_kw * 1000.0
        ydata.append(household_consumption_w)
        line.set_data(range(len(ydata)), list(ydata))
        # x-axis stays fixed, only y-axis auto-scales
        ax.relim()
        ax.autoscale_view()
        # Update the value display
        value_text.set_text(f"Current: {household_consumption_w:.1f} W")
        ax.figure.canvas.draw()
        ax.figure.canvas.flush_events()
        await asyncio.sleep(interval)

def parse_telegram_power(telegram: str):
    # Returns (import_kw, export_kw)
    import_kw = export_kw = 0.0
    m_import = re.search(r"1-0:1\.7\.0\(([\d\.]+)\*kW\)", telegram)
    m_export = re.search(r"1-0:2\.7\.0\(([\d\.]+)\*kW\)", telegram)
    if m_import:
        import_kw = float(m_import.group(1))
    if m_export:
        export_kw = float(m_export.group(1))
    return import_kw, export_kw


async def main():
    async with HomeWizardEnergyV1(host=IP_ADDRESS) as api:
        # Get device information, like firmware version
        print(await api.device())

        print("Real-time power usage (W):")
        try:
            # Initial readings
            interval = 1.0  # seconds

            # Set up the plot
            plt.ion()
            fig, ax = plt.subplots()
            max_points = 60  # Show last 60 seconds
            ydata = deque(maxlen=max_points)
            line, = ax.plot([], [], lw=2)
            ax.set_xlim(0, max_points - 1)
            ax.set_xlabel('Sample')
            ax.set_ylabel('Household Consumption (W)')
            ax.set_title('Real-time Household Power Consumption')
            # Add a text box for the current value
            value_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, va='top', fontsize=12,
                                 bbox=dict(facecolor='white', alpha=0.7))


            await update_plot(api=api, ax=ax, ydata=ydata, line=line, value_text=value_text, interval=interval)
        except KeyboardInterrupt:
            print("Stopped real-time measurement.")


if __name__ == '__main__':
    # get the ip from a text file
    with open('ip.txt', 'r') as f:
        ip = f.read().strip()

    import asyncio
    from homewizard_energy import HomeWizardEnergyV1

    IP_ADDRESS = ip

    asyncio.run(main())