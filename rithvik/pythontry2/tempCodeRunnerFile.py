    found_devices = I2cBusScanner.scan(args.device, not args.no_smb, args.force)
    print("Found I2C devices at addresses:", found_devices)
