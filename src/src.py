from RentalRadar import RentalRadar

def main():
    city = 'west-hartford-ct'
    num_bedrooms = 4

    radar = RentalRadar(city, num_bedrooms)
    radar.scan()

    radar.send_emails()

if __name__ == '__main__':
    main()