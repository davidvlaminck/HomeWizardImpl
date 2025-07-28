

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

            # Get measurements, like energy or water usage
            measurement = await api.measurement()
            print(measurement.energy_import_kwh)

            # Example of getting raw telegram data
            telegram = await api.telegram()
            print(telegram)  # Raw P1 meter data

            # Get all data and remap v1 data to new v2 structure
            v2_model = await api.combined()
            print(v2_model.measurement)
            print(f"normaal elektriciteit: {v2_model.measurement.energy_import_t1_kwh}")
            print(f"dal elektriciteit: {v2_model.measurement.energy_import_t2_kwh}")
            print(f"normaal elektriciteit (injectie): {v2_model.measurement.energy_export_t1_kwh}")
            print(f"dal elektriciteit (injectie): {v2_model.measurement.energy_export_t2_kwh}")
            print(f'actieve power usage: {v2_model.measurement.power_w}')



    asyncio.run(main())