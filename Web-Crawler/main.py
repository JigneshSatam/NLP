from crawler import Crawler


# def main() -> None:
#   # url = "https://www.nasa.gov/black-holes"
#   # url = "https://www.nasa.gov/audience/forstudents/k-4/stories/nasa-knows/what-is-a-black-hole-k4.html"
#   # 1. url = "https://science.nasa.gov/astrophysics/focus-areas/black-holes"
#   # 2. url = "https://www.space.com/15421-black-holes-facts-formation-discovery-sdcmp.html"
#   # url = "https://www.space.com/search?searchTerm=black+holes"


if __name__ == "__main__":
  # main()
  url = "https://www.space.com/15421-black-holes-facts-formation-discovery-sdcmp.html"
  c = Crawler(url)
  c.crawl(50)
