{

    let isSelected = false
    let panel = document.getElementById('profile_change')

     function change () {
          isSelected = !isSelected

          if (isSelected) {
               panel.style.display = 'flex'
          } else {
               panel.style.display = 'none'
          }
     }

}