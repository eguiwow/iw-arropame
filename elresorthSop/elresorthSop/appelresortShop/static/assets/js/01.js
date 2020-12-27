new Vue({
    delimiters : ['[[',']]'],
    el: '#app',
    data: () => {
      return {
         redes:[
				{
					label:'Twitter',
					url:"https://twitter.com/home?lang=es",
					class:"icon brands fa-twitter"
				},
				{
					label:'Facebook',
					url:"https://www.facebook.com/",
					class:"icon brands fa-facebook-f"
				},
				{
					label:'Snapchat',
					url: "https://www.snapchat.com/l/es/",
					class:"icon brands fa-snapchat-ghost"
				},
				{
					label:'Instagram',
					url:"https://www.instagram.com/",
					class:"icon brands fa-instagram"
				},
			]
      }
    }
  })