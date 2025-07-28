

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
                while True:
                    measurement = await api.measurement()
                    print(vars(measurement))
                    net_power = measurement.power_w
                    if net_power >= 0:
                        print(f"Household is using {net_power} W from the grid.")
                    else:
                        print(f"Household is exporting {-net_power} W to the grid (solar overproduction).")
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("Stopped real-time measurement.")

    asyncio.run(main())