window.addEventListener('load', () => {
  Swal.fire({
    title: '您想要播放背景音乐吗?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes',
    cancelButtonText: 'No'
  }).then((result) => {
    if (result.isConfirmed) {
      const audio = new Audio('music/birthday.mp3');
      audio.loop = true;
      audio.play();
    }
    animationTimeline();
  });
});

const animationTimeline = () => {
  const textBoxChars = document.querySelector(".hbd-chatbox");
  const hbd = document.querySelector(".wish-hbd");
  const newText = "亲爱的妈妈，祝您生日快乐！新的一年，我祝愿您身体健健康康，日子平平安安，生活里少些烦恼忧愁，多些悠然自在，被幸福紧紧围绕，在生活中的每一刻都能绽放出快乐的笑容！";
  
  textBoxChars.textContent = newText;
  hbd.textContent = newText;
  textBoxChars.innerHTML = `<span>${textBoxChars.textContent.split("").join("</span><span>")}</span>`;
  hbd.innerHTML = `<span>${hbd.textContent.split("").join("</span><span>")}</span>`;

  const ideaTextTrans = {
    opacity: 0,
    y: -20,
    rotationX: 5,
    skewX: "15deg"
  };

  const ideaTextTransLeave = {
    opacity: 0,
    y: 20,
    rotationY: 5,
    skewX: "-15deg"
  };

  const tl = gsap.timeline();
  tl.to(".container", 0.6, {
    visibility: "visible"
  })
  .from(".one", 0.7, {
    opacity: 0,
    y: 10
  })
  .from(".two", 0.4, {
    opacity: 0,
    y: 10
  })
  .to(".one", 0.7, {
    opacity: 0,
    y: 10
  }, "+=3.5")
  .to(".two", 0.7, {
    opacity: 0,
    y: 10
  }, "-=1")
  .from(".three", 0.7, {
    opacity: 0,
    y: 10
  })
  .to(".three", 0.7, {
    opacity: 0,
    y: 10
  }, "+=3")
  .from(".four", 0.7, {
    scale: 0.2,
    opacity: 0
  })
  .from(".fake-btn", 0.3, {
    scale: 0.2,
    opacity: 0
  })
  .staggerTo(
    ".hbd-chatbox span",
    1.5,
    {
      visibility: "visible"
    },
    0.05
  )
  .to(".fake-btn", 0.1, {
    backgroundColor: "rgb(127, 206, 248)"
  }, "+=4")
  .to(
    ".four",
    0.5,
    {
      scale: 0.2,
      opacity: 0,
      y: -150
    },
    "+=1"
  )
  .from(".idea-1", 0.7, ideaTextTrans)
  .to(".idea-1", 0.7, ideaTextTransLeave, "+=1.5")
  .from(".idea-2", 0.7, ideaTextTrans)
  .to(".idea-2", 0.7, ideaTextTransLeave, "+=1.5")
  .from(".idea-3", 0.7, ideaTextTrans)
  .to(".idea-3 strong", 0.5, {
    scale: 1.2,
    x: 10,
    backgroundColor: "rgb(21, 161, 237)",
    color: "#fff"
  })
  .to(".idea-3", 0.7, ideaTextTransLeave, "+=1.5")
  .from(".idea-4", 0.7, ideaTextTrans)
  .to(".idea-4", 0.7, ideaTextTransLeave, "+=1.5")
  .from(
    ".idea-5",
    0.7,
    {
      rotationX: 15,
      rotationZ: -10,
      skewY: "-5deg",
      y: 50,
      z: 10,
      opacity: 0
    },
    "+=1.5"
  )
  .to(
    ".idea-5 span",
    0.7,
    {
      rotation: 90,
      x: 8
    },
    "+=1.4"
  )
  .to(
    ".idea-5",
    0.7,
    {
      scale: 0.2,
      opacity: 0
    },
    "+=2"
  )
  .staggerFrom(
    ".idea-6 span",
    0.8,
    {
      scale: 3,
      opacity: 0,
      rotation: 15,
      ease: "Expo.easeOut"
    },
    0.2
  )
  .staggerTo(
    ".idea-6 span",
    0.8,
    {
      scale: 3,
      opacity: 0,
      rotation: -15,
      ease: "Expo.easeOut"
    },
    0.2,
    "+=1.5"
  )
  .staggerFromTo(
    ".baloons img",
    2.5,
    {
      opacity: 0.9,
      y: 1400
    },
    {
      opacity: 1,
      y: -1000
    },
    0.2
  )
  .from(
    ".profile-picture",
    0.5,
    {
      scale: 3.5,
      opacity: 0,
      x: 25,
      y: -25,
      rotationZ: -45
    },
    "-=2"
  )
  .from(".hat", 0.5, {
    x: -100,
    y: 350,
    rotation: -180,
    opacity: 0
  })
  .staggerFrom(
    ".wish-hbd span",
    0.7,
    {
      opacity: 0,
      y: -50,
      rotation: 150,
      skewX: "30deg",
      ease: "Elastic.easeOut.config(1, 0.5)"
    },
    0.1
  )
  .staggerFromTo(
    ".wish-hbd span",
    0.7,
    {
      scale: 1.4,
      rotationY: 150
    },
    {
      scale: 1,
      rotationY: 0,
      color: "#ff69b4",
      ease: "Expo.easeOut"
    },
    0.1,
    "party"
  )
  .from(
    ".wish h5",
    0.5,
    {
      opacity: 0,
      y: 10,
      skewX: "-15deg"
    },
    "party"
  )
  .staggerTo(
    ".eight svg",
    1.5,
    {
      visibility: "visible",
      opacity: 0,
      scale: 80,
      repeat: 3,
      repeatDelay: 1.4
    },
    0.3
  )
  .to(".six", 0.5, {
    opacity: 0,
    y: 30,
    zIndex: "-1"
  })
  .from(".ten", 0.7, {
    opacity: 0,
    y: 10
  })
  .to(".last-smile", 0.5, {
    rotation: 90
  }, "+=1");

  const eggs = document.querySelectorAll('.egg');
  const blessingsContainer = document.querySelector('.blessings');
  const blessings = [
    "祝您容颜不老，每天笑意盈盈。",
    "愿您生活如蜜，岁岁幸福美满。",
    "祝您身体硬朗，万事皆能如意。",
    "愿您财运亨通，富贵常伴左右。",
    "祝您心情舒畅，每日无忧无虑。",
    "愿您工作顺利，职场一路坦途。"
  ];

  let eggCount = 0;

  eggs.forEach((egg, index) => {
    function handleClick() {
      if (this.classList.contains('disabled')) return;
      
      this.classList.add('disabled');
      this.style.transform = 'scale(0.9)';
      
      const blessing = document.createElement('p');
      blessing.className = 'blessing';
      blessing.textContent = blessings[index];
      blessingsContainer.appendChild(blessing);
      
      setTimeout(() => {
        this.src = 'img/broken_gold_egg.png';
      }, 200);

      eggCount++;
      if (eggCount === eggs.length) {
        setTimeout(() => {
          gsap.to(".ten", 0.7, {
            opacity: 0,
            visibility: "hidden"
          });
          gsap.to(".nine", 0.7, {
            opacity: 1,
            visibility: "visible"
          });
        }, 5000);
      }
    }
    
    egg.addEventListener('click', handleClick);
  });

  document.getElementById("replay").addEventListener("click", () => {
    window.location.href = 'index.html';
  });
};