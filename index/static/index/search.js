{
     //Default date setter
     second_date =  document.getElementById("second_date")

     let today = new Date()
     let date = null

     let month = today.getMonth()
     month = month +1 >= 10 ? String(month +1) : '0' +String(month +1) 

     let day = today.getDate()
     day = day >= 10 ? String(day) : '0' +String(day) 

     date = today.getFullYear()+'-'+month+'-'+day
     
     second_date.defaultValue = String(date)



     //This must be one of the nastiest codes i've ever written, but i mean idk how to send both forms with no error

     //Fields
     let q_field = document.getElementById("search")
     let f_date_field = document.getElementById("first_date")
     let s_date_field = document.getElementById("second_date")
     let score_field = document.getElementById("score")
     let date_field = document.getElementById("date")
     let inc_field = document.getElementById("increasing")
     let dec_field = document.getElementById("decreasing")
     let both_type_field = document.getElementById("both_type")
     let thread_type_field = document.getElementById("thread")
     let news_type_field = document.getElementById("news")
     let both_state_field = document.getElementById("both_state")
     let open_state_field = document.getElementById("open")
     let answered_state_field = document.getElementById("answered")
     let all_state_field = document.getElementById("all_state")
     let yet_to_happen_state_field = document.getElementById("yet_to_happen")
     let happening_today_state_field = document.getElementById("happening_today")
     let already_happened_state_field = document.getElementById("already_happened")

     let real_q_field = document.getElementById("real_search")
     let real_f_date_field = document.getElementById("real_first_date")
     let real_s_date_field = document.getElementById("real_second_date")
     let real_by_field = document.getElementById("real_by")
     let real_order_field = document.getElementById("real_order")
     let real_type_field = document.getElementById("real_type")
     let real_thread_state_field = document.getElementById("real_thread_state")
     let real_news_state_field = document.getElementById("real_news_state")
     
     /*
     //In case you want to re-check

     console.log(q_field)
     console.log(f_date_field)
     console.log(s_date_field)
     console.log(score_field)
     console.log(date_field)
     console.log(inc_field)
     console.log(dec_field)
     console.log(both_type_field)
     console.log(thread_type_field)
     console.log(news_type_field)
     console.log(both_state_field)
     console.log(open_state_field)
     console.log(asnwered_state_field)
     console.log(all_state_field)
     console.log(yet_to_happen_state_field)
     console.log(happening_today_state_field)
     console.log(already_happened_state_field)
     */


     //Activate / Inactivate fields
     function disableThread (isDisabled) {
          both_state_field.disabled = isDisabled
          open_state_field.disabled = isDisabled
          answered_state_field.disabled = isDisabled

          if (isDisabled) {
               document.getElementById('thread_state_label').className += ' disabled'
               document.getElementById('both_state_label').className += ' disabled'
               document.getElementById('open_label').className += ' disabled'
               document.getElementById('answered_label').className += ' disabled'
          } else {
               document.getElementById('thread_state_label').className = document.getElementById('thread_state_label').className.replace(' disabled', '') 
               document.getElementById('both_state_label').className = document.getElementById('both_state_label').className.replace(' disabled', '')
               document.getElementById('open_label').className = document.getElementById('open_label').className.replace(' disabled', '')
               document.getElementById('answered_label').className = document.getElementById('answered_label').className.replace(' disabled', '')
          }
     }

     function disableNews (isDisabled) {
          all_state_field.disabled = isDisabled
          yet_to_happen_state_field.disabled = isDisabled
          happening_today_state_field.disabled = isDisabled
          already_happened_state_field.disabled = isDisabled

          if (isDisabled) {
               document.getElementById('news_state_label').className += ' disabled'
               document.getElementById('all_state_label').className += ' disabled'
               document.getElementById('yet_to_happen_label').className += ' disabled'
               document.getElementById('happening_today_label').className += ' disabled'
               document.getElementById('already_happened_label').className += ' disabled'
          } else {
               document.getElementById('news_state_label').className = document.getElementById('news_state_label').className.replace(' disabled', '') 
               document.getElementById('all_state_label').className = document.getElementById('all_state_label').className.replace(' disabled', '')
               document.getElementById('yet_to_happen_label').className = document.getElementById('yet_to_happen_label').className.replace(' disabled', '')
               document.getElementById('happening_today_label').className = document.getElementById('happening_today_label').className.replace(' disabled', '')
               document.getElementById('already_happened_label').className = document.getElementById('already_happened_label').className.replace(' disabled', '')    
          }
     }

     function updateFields () {
          if (both_type_field.checked) {
               disableThread(false)
               disableNews(false)
          } else if (thread_type_field.checked) {
               disableThread(false)
               disableNews(true) 
          } else if (news_type_field.checked) {
               disableThread(true)
               disableNews(false) 
          }
     }

     updateFields()

     //Submit, hah more like submissive
     function submitForm () {
         real_q_field.value = q_field.value

         real_f_date_field.value = f_date_field.value
         real_s_date_field.value = s_date_field.value
          
         real_by_field.checked = true
         if (score_field.checked) {
               real_by_field.value = score_field.value
         } else if (date_field.checked) {
               real_by_field.value = date_field.value
         }

         real_order_field.checked = true
         if (inc_field.checked) {
               real_order_field.value = inc_field.value
         } else if (dec_field.checked) {
               real_order_field.value = dec_field.value
         }

         real_type_field.checked = true
         if (both_type_field.checked) {
               real_type_field.value = both_type_field.value
               
               real_thread_state_field.checked = true
               if (both_state_field.checked) {
                    real_thread_state_field.value = both_state_field.value
               } else if (open_state_field.checked) {
                    real_thread_state_field.value = open_state_field.value
               } else if (answered_state_field.checked) {
                    real_thread_state_field.value = answered_state_field.value
               }
          
               real_news_state_field.checked = true
               if (all_state_field.checked) {
                    real_news_state_field.value = all_state_field.value
               } else if (yet_to_happen_state_field.checked) {
                    real_news_state_field.value = yet_to_happen_state_field.value
               } else if (happening_today_state_field.checked) {
                    real_news_state_field.value = happening_today_state_field.value
               } else if (already_happened_state_field.checked) {
                    real_news_state_field.value = already_happened_state_field.value
               }

         } else if (thread_type_field.checked) {
               real_type_field.value = thread_type_field.value

               real_thread_state_field.checked = true
               if (both_state_field.checked) {
                    real_thread_state_field.value = both_state_field.value
               } else if (open_state_field.checked) {
                    real_thread_state_field.value = open_state_field.value
               } else if (answered_state_field.checked) {
                    real_thread_state_field.value = answered_state_field.value
               }

         } else if (news_type_field.checked) {
               real_type_field.value = news_type_field.value

               real_news_state_field.checked = true
               if (all_state_field.checked) {
                    real_news_state_field.value = all_state_field.value
               } else if (yet_to_happen_state_field.checked) {
                    real_news_state_field.value = yet_to_happen_state_field.value
               } else if (happening_today_state_field.checked) {
                    real_news_state_field.value = happening_today_state_field.value
               } else if (already_happened_state_field.checked) {
                    real_news_state_field.value = already_happened_state_field.value
               }
         }

          document.getElementById('real_form').submit()
     }


}