const product = [
    {
        id: 0,
        image: 'image/gg-1.jpg',
        title: 'Builidng a Landing page',
        price: 1,
    },
    {
        id: 1,
        image: 'image/hh-2.jpg',
        title: 'Build your own web server',
        price: 1,
    },
    {
        id: 2,
        image: 'image/ee-3.jpg',
        title: 'To Do App',
        price: 1,
    },
    {
        id: 3,
        image: 'image/aa-1.jpg',
        title: 'E-commerce Website',
        price: 1,
    }
];
const categories = [...new Set(product.map((item)=>
    {return item}))]
    let i=0;
document.getElementById('root').innerHTML = categories.map((item)=>
{
    var {image, title, price} = item;
    return(
        `<div class='box'>
            <div class='img-box'>
                <img class='images' src=${image}></img>
            </div>
        <div class='bottom'>
        <p>${title}</p>
        `+
        "<button onclick='addtocart("+(i++)+")'>Join</button>"+
        `</div>
        </div>`
    )
}).join('')

var cart =[];

function addtocart(a){
    cart.push({...categories[a]});
    displaycart();
}
function delElement(a){
    cart.splice(a, 1);
    displaycart();
}

function displaycart(){
    let j = 0, total=0;
    document.getElementById("count").innerHTML=cart.length;
    if(cart.length==0){
        document.getElementById('cartItem').innerHTML = "Group list empty";
        document.getElementById("total").innerHTML = " "+0+"";
    }
    else{
        document.getElementById("cartItem").innerHTML = cart.map((items)=>
        {
            var {image, title, price} = items;
            total=total+price;
            document.getElementById("total").innerHTML = " "+total+"";
            return(
                `<div class='cart-item'>
                <div class='row-img'>
                    <img class='rowimg' src=${image}>
                </div>
                <p style='font-size:12px;'>${title}</p>
              `+
                "<i class='fa-solid fa-trash' onclick='delElement("+ (j++) +")'></i></div>"
            );
        }).join('');
    }

    
}