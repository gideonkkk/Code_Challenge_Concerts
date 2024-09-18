# main.py
from concerts import Concert, Band, Venue

def main():
    print(Concert.band(1)) 
    print(Concert.venue(1)) 

    beatles = Band(1, "The Beatles", "Liverpool")
    print(beatles.venues())

    madison_square = Venue(1, "Madison Square Garden", "New York")
    print(madison_square.bands())

if __name__ == "__main__":
    main()
