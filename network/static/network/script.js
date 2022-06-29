

function edit_post(id) {
  
  var post_content = document.querySelector(`#post_${id}`).innerHTML;
  document.querySelector(`#postview_${id}`).style.display = "none";
  document.querySelector(`#editview_${id}`).style.display = "block";
  document.querySelector(`#textarea_${id}`).value = post_content;
}

function save_post(id)
{
  var text = document.querySelector(`#textarea_${id}`).value;
  fetch("/edit/" + id, {
    method: "PUT",
    body: JSON.stringify({
      post: text,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      load_page(id)
      document.querySelector(`#post_${id}`).innerHTML = data;
    });

}
 function load_page(id)
 {
   document.querySelector(`#postview_${id}`).style.display = "block";
   document.querySelector(`#editview_${id}`).style.display = "none";

 }
 function like(id)
 {
  const button = document.querySelector(`#liked_${id}`);
  var liked;
   if (button.classList.contains("liked")) {
       liked=false;
     button.classList.remove("liked");
   } else {
     button.classList.add("liked");
      liked = true;
   }
    fetch("/likes/" + id, {
      method: "PUT",
      body: JSON.stringify({
        like: liked,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        document.querySelector(`#likedno_${id}`).innerHTML=data;
      });
    
 }
