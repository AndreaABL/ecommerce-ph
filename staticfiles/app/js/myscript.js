
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



function mostrar() {
    document.getElementById('most').style.display = 'block';
    document.getElementById('ocul').style.display = 'none';
    document.getElementById('atras').style.display = 'block';
    document.getElementById('totalamount').style.display = 'none';
    document.getElementById('correo').style.display = 'none';
}

function atras(){
    document.getElementById('most').style.display='none';
    document.getElementById('atras').style.display='none';
    document.getElementById('ocul').style.display = 'block';
    document.getElementById('totalamount').style.display = 'none';
    document.getElementById('correo').style.display = 'none';

}

function ocultar(){
    document.getElementById('ocul').style.display = 'block';
    document.getElementById('totalamount').style.display = 'block';
    document.getElementById('totalamountt').style.display = 'none';
    document.getElementById('correo').style.display = 'block';
    document.getElementById('info').style.display = 'block';
}

$(function initMap() {

    var input1 = document.getElementById("from");
    var autocomplete1 = new google.maps.LatLng(-34.9860010, -71.0911310);

    input1.innerHTML = autocomplete1;

    var input2 = document.getElementById("to");
    var autocomplete2 = new google.maps.places.Autocomplete(input2);

    
})

var myLatLng = {lat:-34.9860010, lng: -71.0911310};
var mapOptions = {
    center:myLatLng,
    zoom: 7,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
};

var map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);

var directionsService = new google.maps.DirectionsService();

var directionsDisplay = new google.maps.DirectionsRenderer();

directionsDisplay.setMap(map);

var total = document.getElementById('totalamount').value;

function calcRoute() {
    var request = {
        origin: document.getElementById("from").value,
        destination: document.getElementById("to").value,
        travelMode: google.maps.TravelMode.DRIVING,
        unitSystem: google.maps.UnitSystem.METRIC,
    };


    directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            const output = document.querySelector("#output");
            const totalcost = document.querySelector('#totalcost');
            output.innerHTML =
            "<div> <i class='fa-sharp fa-solid fa-road fa-beat-fade' style='font-size:20px; color:#B92508'></i>  : " +
            parseFloat(result.routes[0].legs[0].distance.text) +
            " km</div>";
            totalcost.innerHTML = 
            "<div> <i class='fa-solid fa-sack-dollar fa-bounce' style='font-size:20px; color:#B9A708'></i> : $" + parseFloat(result.routes[0].legs[0].distance.text) * parseFloat(1472) + "</div>";        
            
            var totalcos = parseFloat(result.routes[0].legs[0].distance.text) * parseFloat(1472)
            var totalfinal = Number(total) + (totalcos)

            
            document.getElementById('totalamountt').value = totalfinal;
            document.getElementById('totalamountt').style.display = 'block';
            document.getElementById('totalamount').style.display = 'none';
            document.getElementById('correo').style.display = 'block';
            document.getElementById('info').style.display = 'block';
            

        
        directionsDisplay.setDirections(result);    
        } else {
            directionsDisplay.setDirections({routes: []});
            map.setCenter(myLatLng);
            output.innerHTML = 
            "<div class='alert-danger'><i class='fas fa-exclamation-triangle' style='color:red'></i> No se pudo recuperar la distancia de conducción. </div>";
        }
    });
}

$('.costototal').click(function(){
    var id=$(this).attr("totalcost").toString();
    console.log("pid =", id)
    $.ajax({
        type:'GET',
        url:'/costototal',
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("data = " ,data);
            document.getElementById('amount').innerText=data.amount
            document.getElementById('totalcost').innerText=data.totalamount
        }
    })
})

const $form = document.querySelector('#form')

$form.addEventListener('submit', handleSubmit)
async function handleSubmit(event) {
    event.preventDefault()
    const form = new FormData(this)
    const response = await fetch(this.action, {
        method:this.method,
        body:form, 
        headers: {
            'Accept':'application/json'
        }
    })
    if (response.ok) {
        this.reset()
        alert('Gracias por enviar tu información, te contactaremos a la brevedad')
    }
}

//const form = document.getElementById("form");


//form.addEventListener('submit', function(e) {
//    e.preventDefault();

  //  const payload = new FormData(form)


    //console.log([...payload])

    //fetch('/checkout' , {
      //  method:'POST',
       // body: payload,
    //})
    //.then(res=> res.json())
    //.then(data => console.log(data))
    //.catch(err=>console.log(err));
    
//})

