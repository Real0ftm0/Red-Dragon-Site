// show cart

(function(){
    const cartinfo = document.getElementById('cart-info');
    const cart = document.getElementById('cart');

    cartinfo.addEventListener('click', function(){
    cart.classList.toggle('show-cart');
    });
})();
// add items to cart

(function(){

const cartBtn = document.querySelectorAll('.menu-add-cart');

 cartBtn.forEach(function(btn){
    btn.addEventListener('click',function(Event){
      //  console.log(Event.target);
      if(Event.target.parentelement.classList.contains('menu-add-cart')){
        console.log(Event.target.parentelement.previousElementSibling)
      }
    });
 });
})();



// loop thorough data and display each field
function displayData(data) {
  data.items.forEach((item, index) => {
    const div = document.createElement('div');
    div.classList.add('product-item');
    div.id = item.sys.id;

    div.innerHTML = `
          <div class="product__${index + 1}">
          <h3 class="product__${index + 1}--title">${item.fields.title}</h3>
          <div class="product__${index + 1}--image">
          <img
              class="image--${index + 1}"
              src="${item.fields.image.fields.file.url}"
              alt="product ${index + 1}"
              class="product-image"
          />
          </div>
          <h5 class="product__1--price">${item.fields.price} $</h5>
          <button class="btn add-cart">Add product</button>
          </div>
      `;

    productContainer.append(div);
  });

  loadListeners();
  loadPreviousCart();
  loadPreviousQtyCart();
}

function loadListeners() {
  const addCartBtn = document.querySelectorAll('.add-cart');

  addCartBtn.forEach((btn) => btn.addEventListener('click', handleAddProduct));
}

function loadPreviousCart() {
  const prevCart = getLocalStorage('currentCart');
  currentCart = prevCart ? prevCart : [];
  prevCart && displayCartItems(currentCart);
}

function loadPreviousQtyCart() {
  displayCartIcon('initialState');
}