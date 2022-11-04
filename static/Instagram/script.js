const stories = document.getElementsByClassName("stories")[0];
stories.addEventListener("wheel", (e) => {
  stories.scrollLeft += e.deltaY;
});
// main work for story
const csrf = Cookies.get('csrftoken');

const story = document.getElementsByClassName("story"); // ==> container of story
const main = document.getElementsByClassName("main_story")[0]; // ==> full screen story
const story_image = document.getElementById("story_image"); //==> main story
const storY = document.getElementById("story"); //==> full screen stroy
Array.from(story).forEach((element) => {
  element.addEventListener("click", () => {
    main.style.display = "block";
    console.log(element.childNodes);
    let src = element.childNodes[1].src;
    console.log(src);
    storY.setAttribute("src", src);
  });
});
main.onclick = () => {
  main.style.display = "none";
};

document.querySelectorAll(".likeBtn").forEach((item)=>{
item.addEventListener('click',()=>{
  var url = 'like/'+item.dataset.id
  var like_curr_user;
fetch(url,{
  method: "POST",
  headers: {'X-CSRFToken': csrf},
}).then(e => e.json()).then((data) => {
  if(data.like)
  {
    item.innerHTML = `<i class="fa fa-heart liked" style="font-size:20px;"></i>`;
  }
  else{
    item.innerHTML =`<i class="fa fa-heart-o nol" aria-hidden="true" style="font-size:20px;"></i>`;
  }

  i = "span-"+item.dataset.id
  document.getElementById(i).innerHTML = String(data.count+" likes");
})


})


})