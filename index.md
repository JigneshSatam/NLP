---
layout: default
title: NLP
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
                {% if topic.topics_covered %}
                  <h3>Topics covered</h3>
                  <ul>
                    {% for topic_covered in topic.topics_covered %}
                      <li>{{ topic_covered }}</li>
                    {% endfor %}
                  </ul>
                {% endif %}
              </div>
            </div>
          </div>
        {% endfor %}
      </div>
    </div>
  </div>
</body>
