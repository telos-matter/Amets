{

     let isSelected = false
     let panel = document.getElementById('language_panel')

     function select () {
          isSelected = !isSelected

          if (isSelected) {
               panel.style.display = 'flex'
          } else {
               panel.style.display = 'none'
          }
     }
}