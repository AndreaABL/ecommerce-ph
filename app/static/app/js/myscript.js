document.addEventListener("DOMContentLoaded", function () {
  const adContainer = document.getElementById("ad-container");

  // Display the ad with an effect
  function showAd() {
      adContainer.style.display = "flex";
  }

  // Close the ad when clicking anywhere on the screen
  function closeAd() {
      adContainer.style.display = "none";
  }

  // Listen for clicks on the ad container
  adContainer.addEventListener("click", closeAd);

  // Show the ad after a delay (e.g., 5 seconds)
  setTimeout(showAd, 400);
});

$('.plus-cart').click(function(){
  var id = $(this).attr("pid").toString();
  var eml = this.parentNode.children[2]
  console.log("pid =", id)
  $.ajax({
      type:'GET',
      url:'/pluscart',
      data:{
          prod_id:id
      },
      success:function(data){
          console.log("data = " ,data);
          eml.innerText=data.quantity
          document.getElementById('amount').innerText=data.amount
          document.getElementById('totalamount').innerText=data.totalamount
      }
  })
})

$('.minus-cart').click(function(){
  var id=$(this).attr("pid").toString();
  var eml=this.parentNode.children[2]
  $.ajax({
      type:'GET',
      url:'/minuscart',
      data:{
          prod_id:id
      },
      success:function(data){
          eml.innerText=data.quantity
          document.getElementById('amount').innerText=data.amount
          document.getElementById('totalamount').innerText=data.totalamount
      }
  })

})

$('.remove-cart').click(function(){
  var id=$(this).attr("pid").toString();
  var eml=this
  $.ajax({
      type:'GET',
      url:'/removecart',
      data:{
          prod_id:id 
      },
      success:function(data){
          document.getElementById('amount').innerText=data.amount
          document.getElementById('totalamount').innerText=data.totalamount
          eml.parentNode.parentNode.parentNode.parentNode.remove()
      }
  })
})



document.getElementById('delivery_option').addEventListener('change', function() {
  var locationField = document.getElementById('location_field');
  if (this.value === 'despacho') {
      locationField.style.display = 'block';
  } else {
      locationField.style.display = 'none';
  }
});


const sendButton = document.getElementById("sendButton");
const notification = document.getElementById("notification");

  // Add a click event listener to the button
sendButton.addEventListener("click", function () {
      // Show the notification when the button is clicked
  notification.style.display = "block";

      // Hide the notification after a certain time (e.g., 3 seconds)
  setTimeout(function () {
      notification.style.display = "none";
  }, 5000);
});

function showAddress() {
  var addressInfo = document.getElementById('address-info');
  var contactInfo = document.getElementById('contact-info');
  var emailInfo = document.getElementById('email-info');
  var timeInfo = document.getElementById('time-info');

  addressInfo.style.display = 'block';
  contactInfo.style.display = 'none';
  emailInfo.style.display = 'none';
  timeInfo.style.display = 'none';
}

// Function to show CSS information
function showContact() {
  var addressInfo = document.getElementById('address-info');
  var contactInfo = document.getElementById('contact-info');
  var emailInfo = document.getElementById('email-info');
  var timeInfo = document.getElementById('time-info');

  addressInfo.style.display = 'none';
  contactInfo.style.display = 'block';
  emailInfo.style.display = 'none';
  timeInfo.style.display = 'none';
}

function showEmail() {
  var addressInfo = document.getElementById('address-info');
  var contactInfo = document.getElementById('contact-info');
  var emailInfo = document.getElementById('email-info');
  var timeInfo = document.getElementById('time-info');

  addressInfo.style.display = 'none';
  contactInfo.style.display = 'none';
  emailInfo.style.display = 'block';
  timeInfo.style.display = 'none';
}

function showTime() {
  var addressInfo = document.getElementById('address-info');
  var contactInfo = document.getElementById('contact-info');
  var emailInfo = document.getElementById('email-info');
  var timeInfo = document.getElementById('time-info');

  addressInfo.style.display = 'none';
  contactInfo.style.display = 'none';
  emailInfo.style.display = 'none';
  timeInfo.style.display = 'block';
}


