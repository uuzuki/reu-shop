document.addEventListener('DOMContentLoaded', function() {
  const tabs = document.querySelectorAll('.auth-tab');
  const forms = document.querySelectorAll('.form-content');
  
  tabs.forEach((tab, index) => {
      tab.addEventListener('click', function(e) {
          e.preventDefault();

          tabs.forEach(t => t.classList.remove('active'));
          forms.forEach(f => f.classList.remove('active'));

          this.classList.add('active');

          forms[index].classList.add('active');
      });
  });
});