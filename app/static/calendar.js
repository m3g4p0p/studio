window.addEventListener('DOMContentLoaded', () => {
  const target = document.querySelector('.highlight, .today')

  if (!target) {
    return
  }

  target.scrollIntoView({
    behavior: 'smooth',
    block: 'center'
  })
})
