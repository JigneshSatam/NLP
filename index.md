---
layout: default
title: NLP
---

<div class="row g-2">
  <h2>Topics</h2>
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
            <p>
              {% if topic.folder %} | <a href="https://github.com/jigneshsatam/NLP/tree/main/{{topic.folder}}">View on GitHub</a> {% endif %}
              {% if topic.report %} | <a href="{{topic.report}}">Report</a> {% endif %} |
            </p>
          </div>
        </div>
      </div>
    {% endfor %}
  </div>
  <p></p>
</div>
<div class="row g-2">
  <h2>Technical Skills</h2>
  <ul>
    <li>Natural Language Processing</li>
    <li>Python</li>
    <li>Jupyter Notebooks</li>
    <li>Git</li>
    <li>Jekyll</li>
    <li>Machine Learning</li>
  </ul>
  <p>
  </p>
</div>
<div class="row g-2">
  <h2>Soft Skills</h2>
  <ul>
    <li>Communication: During team meetings, I listen carefully to your colleague's concerns and suggestions, and then summarize what you heard to ensure that you understood their perspective correctly.</li>
    <li>Scheduling: I have several tasks to complete by in a sprint, so I prioritize them based on their importance and deadline, and work on the most urgent ones first.</li>
    <li>Time and Project Management: I am working on a long-term project, so I break it down into smaller, more manageable goals with clear deadlines, and regularly review my progress to ensure that I are on track.</li>
    <li>Analytical Thinking: In a case of any problem in the project, I gather and analyze data, brainstorm potential solutions, and then evaluate and implement the most effective option.</li>
    <li>Flexibility: My company had a major reorganization, so I adapt to the new structure and responsibilities, and look for ways to contribute to the team's success in the new environment.</li>
    <li>Ability to Work in a Team or Independently: I work on a team project, so you communicate effectively with your colleagues, share ideas, and collaborate on tasks to achieve the project goals. Alternatively, I work independently on a task, but reach out to colleagues when I need help or feedback.</li>
  </ul>
  <p>
  </p>
</div>
<div class="row g-2">
  <h2>About Me</h2>
  <p>I am passionate about NLP and constantly seek to learn more about this rapidly changing field. I have plans to work on personal projects that involve creating a chatbot using deep learning and building a recommendation system for online news articles. To keep up with the latest developments, I read research papers, participate in online communities, and attend conferences and workshops.</p>
  <p>I am also interested in possible employment opportunities that allow me to apply my skills and contribute to the NLP community.</p>
</div>

<div class="row g-2">
  <h2>Special Thanks</h2>
  <p>
    Grateful for <a href="https://github.com/kjmazidi">Dr. Mazidi, Karen's</a > exceptional dedication to teaching and creating a supportive learning environment.
  </p>
