---
layout: default
title: Final
---

<body>
  <div class="container">
    <div class="row g-2">
      <div class="accordion" id="accordionExample">
        {% for topic in site.data.topics %}
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingOne">
              <button class="accordion-button {{topic.collapsed}}" type="button" data-bs-toggle="collapse" data-bs-target="#{{ topic.label }}" aria-expanded="true" aria-controls="{{ topic.label }}">
                {{ topic.name }}
              </button>
            </h2>
            <div id="{{ topic.label }}" class="accordion-collapse collapse {{ topic.class }}" aria-labelledby="{{ topic.label }}" data-bs-parent="#accordionExample">
              <div class="accordion-body">
                <p>{% if topic.img %}
                  <img src="{{ topic.img }}" alt="topic.name"/>
                {% endif %}</p>
                {% for description in topic.descriptions %}
                  <p>{{ description }}</p>
                {% endfor %}
                <p>The project covers topics such as:</p>
                <ul>
                  <li>Natural Language Processing (NLP) fundamentals</li>
                  <li>Data pre-processing and preparation</li>
                  <li>Training and testing machine learning models</li>
                  <li>Performance evaluation and optimization</li>
                </ul>
              </div>
            </div>
          </div>
        {% endfor %}
      </div>
    </div>
  </div>
</body>
