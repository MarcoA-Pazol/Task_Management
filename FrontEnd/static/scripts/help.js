document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.question').forEach(question => {
      question.addEventListener('click', () => {
        // Encuentra la respuesta correspondiente para la pregunta actual
        const answer = question.nextElementSibling;
    
        // Alterna la visibilidad de la respuesta
        if (answer.style.display === 'block') {
          answer.style.display = 'none';
        } else {
          answer.style.display = 'block';
        }
      });
    });
  });