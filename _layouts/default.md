<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% if page.title %}{{ page.title }} | {% endif %}{{ site.title }}</title>

  <!-- Bootstrap 5 CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css">

  <!-- Bootstrap JS and jQuery -->
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>

  <div class="container my-4">
    <div class="row g-2">
      <div class="col-md-12 mx-auto">
        <h1 class="text-center mb-5">NLP</h1>
        <p>
          Natural Language Processing (NLP) is a subfield of Artificial Intelligence that focuses on the interaction between computers and humans using natural language. The goal of NLP is to enable computers to understand, interpret, and generate human language in a way that is meaningful and useful.
        <br/>
          NLP involves a variety of tasks, such as text classification, sentiment analysis, named entity recognition, machine translation, question answering, and speech recognition. These tasks are often achieved using machine learning and deep learning techniques, such as neural networks.
        </p>
        <p>
          NLP has many practical applications, including chatbots, virtual assistants, sentiment analysis for social media monitoring, automated translation services, and text-to-speech systems. NLP is also used in the field of healthcare for clinical decision support and electronic health record management.
        <br/>
          As the amount of text data continues to grow, the importance of NLP in business and research is becoming increasingly evident. The development of new algorithms and techniques is advancing the field, and there is a growing need for professionals with NLP expertise in a variety of industries.
        </p>
        <p>
        <a href="Overview%20of%20NLP.pdf">READ MORE</a>
        </p>
      </div>
    </div>
    {{ content }}
  </div>
</body>
</html>
