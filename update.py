import requests
from bs4 import BeautifulSoup

URL = "https://hospitaldeamor.com.br/site/noticias/"

def fetch_news():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Cada notícia é um <article class="et_pb_post">
    items = soup.select("article.et_pb_post")[:10]

    news_list = []

    for item in items:
        # Imagem
        img_tag = item.select_one(".et_pb_image_container img")
        image = img_tag["src"] if img_tag else ""

        # Título
        title_tag = item.select_one("h3.entry-title a")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Link
        link = title_tag["href"] if title_tag else ""

        # Resumo
        summary_tag = item.select_one(".post-content-inner p")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""

        news_list.append({
            "title": title,
            "link": link,
            "summary": summary,
            "image": image
        })

    return news_list


def generate_html(news):
    html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Mural de Notícias - Hospital de Amor</title>
<style>
  body {
    margin: 0;
    padding: 0;
    width: 830px;
    height: 500px;
    background: #0A1A3A;
    font-family: Arial, sans-serif;
    color: white;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .slider {
    position: relative;
    width: 830px;
    height: 500px;
  }

  .slide {
    position: absolute;
    width: 830px;
    height: 500px;
    opacity: 0;
    transition: opacity 1.5s ease-in-out;
  }

  .slide.active {
    opacity: 1;
  }

  .slide img {
    width: 100%;
    height: 280px;
    object-fit: cover;
    border-radius: 6px;
  }

  .content {
    padding: 15px;
  }

  h3 {
    margin: 10px 0 5px;
    font-size: 22px;
  }

  p {
    font-size: 18px;
  }
</style>
</head>
<body>

<div class="slider">
"""

    for n in news:
        html += f"""
        <div class="slide">
          <img src="{n['image']}" alt="Notícia">
          <div class="content">
            <h3>{n['title']}</h3>
            <p>{n['summary']}</p>
          </div>
        </div>
        """

    html += """
</div>

<script>
  let slides = document.querySelectorAll('.slide');
  let index = 0;

  function showSlide() {
    slides.forEach((s, i) => {
      s.classList.remove('active');
      if (i === index) s.classList.add('active');
    });

    index = (index + 1) % slides.length;
  }

  showSlide();
  setInterval(showSlide, 6000);
</script>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    news = fetch_news()
    generate_html(news)
