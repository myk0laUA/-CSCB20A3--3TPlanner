
//my_day.html JS code

function updateTimers() {
    const timers = document.querySelectorAll('.timer');
    const now = new Date();
    timers.forEach(timer => {
    const duration = parseInt(timer.getAttribute('data-duration'), 10);
    const startTimeUtc = new Date(timer.getAttribute('data-start-time'));
    const startTime = new Date(startTimeUtc.getTime() - startTimeUtc.getTimezoneOffset() * 60000);
    const timeLeft = startTime.getTime() + duration * 60000 - now.getTime();
    const minutesLeft = Math.floor(timeLeft / 60000);
    const secondsLeft = Math.floor((timeLeft % 60000) / 1000);
    timer.textContent = `${minutesLeft} min ${secondsLeft} sec`;
    if (timeLeft <= 0) {
      location.reload();
    }
});
}

setInterval(updateTimers, 1000);

// JavaScript code from tips.html
$(document).ready(function() {
    $('.modal').on('shown.bs.modal', function() {
        $(this).find('[autofocus]').focus();
    });
});



// Smooth Transitions between the pages

document.addEventListener('DOMContentLoaded', function () {
    var pageContent = document.getElementById('page-content');
    if (pageContent) {
      pageContent.style.opacity = 1;
    }
  });