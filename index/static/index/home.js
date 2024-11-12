{
     
     let index  = -1
     let slides = document.getElementsByClassName('slide')
     let dots = document.getElementsByClassName('dot')
     
     autoNext()

     function autoNext () {
          nextSlide()
          setTimeout(autoNext, 7000)
     }
     
     function prevSlide () {  
          showSlide(index -1)
     }
     
     function nextSlide () {
          showSlide(index +1)
     }
     
     function validateIndex () {
          if (index < 0) {
               index = slides.length -1
          } else if (index >= slides.length) {
               index = 0
          }
     }
     
     function showSlide (n) {
          index = n
          validateIndex()

          for (let i = 0; i < slides.length; i++) {
               if (i == index) {
                    slides[i].style.display = 'flex'
                    dots[i].className += " active";
               } else {
                    slides[i].style.display = 'none'
                    dots[i].className = dots[i].className.replace(" active", "");
               }
          }   
     }

}