let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['SG']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
        
    }
    // get the address components and assign them to the fields
    var geocoder= new google.maps.Geocoder()
    var address = document.getElementById('id_address').value
    geocoder.geocode({'address':address},function(results,status){
        if(status==google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            $('#id_latitude').val(latitude)
            $("#id_longitude").val(longitude)
            $('#id_address').val(address)
        }
    });

    console.log(place)
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            if(place.address_components[i].types[j]=="country"){
                $('#id_country').val(place.address_components[i].long_name)
            }
            else if(place.address_components[i].types[j]=="locality"){
                $('#id_state').val(place.address_components[i].long_name)
            }
            else if(place.address_components[i].types[j]=="neighborhood"){
                $('#id_city').val(place.address_components[i].long_name)
            }
            else if(place.address_components[i].types[j]=="postal_code"){
                $('#id_zip_code').val(place.address_components[i].long_name)
            }
        }
        
    }
}


$(document).ready(function(){
    $('.add_to_cart').on('click',function(e){
        e.preventDefault()
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = {
            food_id: food_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data:data,
            success: function(response){
                console.log(response.cart_counter['cart_count'])
                $('#cart_counter').html(response.cart_counter['cart_count'])
                $('#qty-'+food_id).html(response.qty)
                $('#subtotal').html(response.price['cart_price'])
                $('#tax').html(response.price['tax_amount'])
                $('#total').html(response.price['total'])
                console.log(response.price['cart_price'])
                console.log(response.price['tax_amount'])
                console.log(response.price['total'])
                
            }
            
        })
    })
    $('.decrease_cart').on('click',function(e){
        e.preventDefault()
        url = $(this).attr('data-url')
        food_id= $(this).attr('data-id')
        cart_id = $(this).attr('data-id-2')
        data = {
            food_id: food_id,
            cart_id: cart_id
        }
        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                console.log(response)
                if(response.status=='item_not_in_cart'){
                    Swal.fire('This Item is not in the cart yet')
                }else{
                $('#cart_counter').html(response.cart_counter['cart_count'])
                $('#qty-'+food_id).html(response.qty)
                $('#subtotal').html(response.price['cart_price'])
                $('#tax').html(response.price['tax_amount'])
                $('#total').html(response.price['total'])
                if(response.qty=='0'){
                    removeCartItem(0,cart_id)
                    checkcartempty()
                }
            }
            }
        })
        
    })
    $('.delete_cart').on('click',function(e){
        e.preventDefault()
        url = $(this).attr('data-url')
        cart_id= $(this).attr('data-id')
        data = {
            cart_id: cart_id,
        }
        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                console.log(response)
                $('#cart_counter').html(response.cart_counter['cart_count'])
                removeCartItem(0,cart_id)
                checkcartempty()
                $('#subtotal').html(response.price['cart_price'])
                $('#tax').html(response.price['tax_amount'])
                $('#total').html(response.price['total'])
                
            
            }
        })
        
    })
    // delete cart element if the qwty is 0
    function removeCartItem(cartitemqty,cart_id){
        
            if(cartitemqty<=0){
                document.getElementById("cart-item-"+cart_id).remove()
                console.log()
            
        }
        
    }
    function checkcartempty(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter==0){
            document.getElementById('empty_cart').style.display = 'block'
        }
    }

    // load subtotal on load 
    
   
    // place the cart item quantity on load
    $('.item-qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })


    $('.add_hour').on('click',function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken').val()
        var url = document.getElementById('add_hour_url').value

        if(is_closed){
            is_closed = 'True'
            condition = day !='' 
        }else{
            is_closed = "False"
            condition = day !='' && from_hour != '' && to_hour != ''
        }

        if(eval(condition)){
            $.ajax({
                type: 'POST',
                url:url,
                data: {
                    'day':day,
                    'from_hour':from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token,

                },
                success: function(response){
                    if(response.status == 'success'){
                       if(response.is_closed == 'Closed'){
                        html='<tr><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="">Remove</a></td></tr>'

                       }else{
                        html='<tr><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+ response.to_hour+'</td><td><a href="">Remove</a></td></tr>'

                       }
                       $('.opening_hours').append(html)
                       document.getElementById('opening_hours').reset();

                    }else{
                        Swal.fire(response.message)
                    }
                }
            })
    
        }else{
            Swal.fire('Please fill in all fields')
        }
        
    })

    $('.remove_opening_hours').on('click',function(e){
        e.preventDefault()
        url = $(this).attr('data-url')
        hour_id = $(this).attr('data-id')
        $.ajax({
            type: 'GET',
            url:url,
            data: {
                'hour_id': hour_id,

            },
            success: function(response){
                alert('Item has been removed')
                $('#opening_hour-'+hour_id).remove();
            }
        })

    })



    // document ready close 

    
})