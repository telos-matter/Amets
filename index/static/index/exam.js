{
          
     seconds_left = 601

     time_label =  document.getElementById("time_label")
     form = document.getElementById("exercise_form") 

     function updateLabel () {
          min = Math.floor(seconds_left/60)
          sec = seconds_left%60
          time_label.innerHTML = String(min +':' +sec +' left') 
     }

     function tick () {
          seconds_left--
          updateLabel()

          if (seconds_left == 0) {
               form.submit()
          }

          setTimeout(tick, 1000)
     }

     tick()

}