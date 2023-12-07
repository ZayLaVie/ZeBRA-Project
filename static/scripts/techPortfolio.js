const product = [
    {
        id: 0,
        image: 'https://blog.digitalcook.fr/wp-content/uploads/2021/04/Landing-Page.png',
        title: 'Builidng a Landing page',
        price: 1,
    },
    {
        id: 1,
        image: 'https://tse1.mm.bing.net/th?id=OIP.sDkW6w1i7ET_BaR_UMonHQHaI3&pid=Api&P=0&h=220',
        title: 'Build your own web server',
        price: 1,
    },
    {
        id: 2,
        image: 'https://www.pinclipart.com/picdir/big/117-1176996_checklist-clipart.png',
        title: 'To Do App',
        price: 1,
    },
    {
        id: 3,
        image: 'https://www.zeumic.com.au/wp-content/uploads/2018/04/zeumic-e-commerce-cycle-st-kilda-image.jpg',
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