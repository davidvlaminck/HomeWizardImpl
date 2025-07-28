

if __name__ == '__main__':
    # get the ip from a text file
    with open('ip.txt', 'r') as f:
        ip = f.read().strip()

    import asyncio
    from homewizard_energy import HomeWizardEnergyV1

    IP_ADDRESS = ip


    async def main():
        async with HomeWizardEnergyV1(host=IP_ADDRESS) as api:
            # Get device information, like firmware version
            print(await api.device())

            print("Real-time power usage (W):")
            try:
                # Initial readings
                prev = await api.measurement()
                prev_import = prev.energy_import_t1_kwh + prev.energy_import_t2_kwh
                prev_export = prev.energy_export_t1_kwh + prev.energy_export_t2_kwh
                interval = 5.0  # seconds

                import re

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

                interval = 1.0  # seconds

                while True:
                    telegram = await api.telegram()
                    import_kw, export_kw = parse_telegram_power(telegram)
                    household_consumption_kw = import_kw + export_kw
                    household_consumption_w = household_consumption_kw * 1000.0
                    print(f"Estimated household consumption: {household_consumption_w:.1f} W (interval: {interval}s)")
                    await asyncio.sleep(interval)
            except KeyboardInterrupt:
                print("Stopped real-time measurement.")

    asyncio.run(main())