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

<!-- Fonte Inter -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">

<style>
  body {
    margin: 0;
    padding: 0;
    width: 830px;
    height: 500px;
    background: #0A1A3A;
    font-family: 'Inter', sans-serif;
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
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 0 25px rgba(0,0,0,0.4);
  }

  .slide {
    position: absolute;
    width: 830px;
    height: 500px;
    opacity: 0;
    transition: opacity 3s ease-in-out;
  }

  .slide.active {
    opacity: 1;
  }

  .image-area {
    width: 100%;
    height: 260px;
    overflow: hidden;
  }

  .image-area img {
    width: 100%;
    height: 260px;
    object-fit: cover;
  }

  /* ✅ Degradê aplicado atrás da notícia */
  .content {
    padding: 18px;
    height: 240px;
    background: linear-gradient(135deg, #1E3C72, #2A5298);
    border-bottom-left-radius: 14px;
    border-bottom-right-radius: 14px;
  }

  h3 {
    margin: 5px 0 10px;
    font-size: 22px;
    font-weight: 600;
  }

  p {
    font-size: 17px;
    line-height: 1.35;
    font-weight: 300;
  }

  /* Indicadores */
  .dots {
    position: absolute;
    bottom: 12px;
    width: 100%;
    text-align: center;
  }

  .dot {
    display: inline-block;
    width: 12px;
    height: 12px;
    margin: 0 4px;
    background: rgba(255,255,255,0.4);
    border-radius: 50%;
    transition: background 0.3s;
  }

  .dot.active {
    background: #fff;
  }
</style>
</head>
<body>

<div class="slider">
"""

    # ✅ Loop corrigido (sem duplicação)
    for n in news:
        html += f"""
<div class="slide">
  <div class="image-area">
    <img src="{n['image']}" alt="Notícia">
  </div>
  <div class="content">
    <h3>{n['title']}</h3>
    <p>{n['summary']}</p>
  </div>
</div>
"""

    html += """
<div class="dots"></div>

</div>

<script>
  let slides = document.querySelectorAll('.slide');
  let dotsContainer = document.querySelector('.dots');
  let index = 0;

  // Criar indicadores
  slides.forEach((s, i) => {
    let d = document.createElement('div');
    d.classList.add('dot');
    if (i === 0) d.classList.add('active');
    dotsContainer.appendChild(d);
  });

  let dots = document.querySelectorAll('.dot');

  function showSlide() {
    slides.forEach(s => s.classList.remove('active'));
    dots.forEach(d => d.classList.remove('active'));

    slides[index].classList.add('active');
    dots[index].classList.add('active');

    index = (index + 1) % slides.length;
  }

  showSlide();
  setInterval(showSlide, 15000);
</script>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    news = fetch_news()
    generate_html(news)
