$(document).ready(function(){
	var formBasket = $('#form_bay_prod_datail');
	var formFilter = $('#filter');
	var sortBy= $('#sort_by');
	var reviewStar = $('.review-rating');
	$.each( reviewStar, function( index, value ){
		var rating = $(value).data('star');
		var countStar = $(value).data('count');
		var idStar = $(value).attr('id');//$(value).id
		(rating >= 1) ?  $('#'+idStar).append('<i class="fa fa-star" aria-hidden="true"></i>') : $('#'+idStar).append('<i class="far fa-star" aria-hidden="true"></i>');
		(rating >= 2) ?  $('#'+idStar).append('<i class="fa fa-star" aria-hidden="true"></i>') : $('#'+idStar).append('<i class="far fa-star" aria-hidden="true"></i>');
		(rating >= 3) ?  $('#'+idStar).append('<i class="fa fa-star" aria-hidden="true"></i>') : $('#'+idStar).append('<i class="far fa-star" aria-hidden="true"></i>');
		(rating >= 4) ?  $('#'+idStar).append('<i class="fa fa-star" aria-hidden="true"></i>') : $('#'+idStar).append('<i class="far fa-star" aria-hidden="true"></i>');
		(rating >= 5) ?  $('#'+idStar).append('<i class="fa fa-star" aria-hidden="true"></i>') : $('#'+idStar).append('<i class="far fa-star" aria-hidden="true"></i>');
		{countStar&&$('#'+idStar).append('<span> '+countStar+'</span> ')};
		console.log(rating + idStar + ' '+countStar);
		
	})
	//console.log(reviewStar);
	var page=1;
	var buttonGridList=1;
	var sortVal=0;
	$('.category').hide();


	function basketUpdate(product_id, qty, is_delete){
		var data = {};
		data.product_id=product_id;
		data.nmb = qty;
		var csrf_token = $('#csrf_hiden_code [name="csrfmiddlewaretoken"]').val();
		data["csrfmiddlewaretoken"] = csrf_token;

		if (is_delete){
			data["is_delete"] = true;
			}

		var url="/basket_adding/"
		
		$.ajax({
			url: url,
			type: 'POST',
			data: data,
			cache: true,
			success: function(data){
				console.log("OK");
				console.log(data.product_total_num);
				console.log(data.product);
				if (data.product_total_num || data.product_total_num==0){
				$('#cart_total_qty').text(data.product_total_num);
				var cart_total_amount=0;
				$('.cart-list').html("");
				$.each(data.product, function(k, v){
					$('.cart-list').append('<li><div class="cart-item-desc">\
                            <a href="#" class="image">\
                            <img src="'+v.product_image+'" class="cart-thumb" alt=" ">\
                            </a>\
                            <div>\
                                <a href="#" style="color:red">'+v.name+'</a>\
                                <p>'+v.nmb+' x - <span class="price">'+v.price_per_item+' ₽</span></p>\
                            </div>\
                        </div>\
                        <span class="dropdown-product-remove" data-product_id="'+v.id+'"><i class="fas fa-trash-alt"></i></span>\
                        </li>');
					cart_total_amount +=parseInt(v.nmb)*parseInt(v.price_per_item);
				})
				$('#cart_total_amount').text(cart_total_amount);
			  }
			},
			error: function(){
				console.log('error');
			}
		})
	}



	formBasket.on('submit', function(e){
		e.preventDefault();

		var qty= $('#qty2').val();
		console.log(qty);
		var sumit_btn = $('#btn_submit');
		var product_id = sumit_btn.data("product_id");
		var product_name = sumit_btn.data("product_name");
		var product_price = sumit_btn.data("product_price");
		var product_url = sumit_btn.data("product_url");
		//var url=form.attr("action");
		//var csrf_token = $('#form_bay_prod_datail [name="csrfmiddlewaretoken"]').val(); //   csrf_hiden_code
		console.log(product_name);

		basketUpdate(product_id, qty, is_delete=false)


		/*$('.cart-list').append('<li><div class="cart-item-desc">\
                              <a href="#" class="image">\
                              <img src="'+product_url+'" class="cart-thumb" alt="">\
                              </a>\
                              <div>\
                                  <a href="#" style="color:red">'+product_name+'</a>\
                                  <p>'+qty+' x - <span class="price">'+product_price+' ₽</span></p>\
                              </div>\
                          </div>\
                          <span class="dropdown-product-remove" data-product_id="'+v.id+'"><i class="fas fa-trash-alt"></i></span>\
                          </li>');*/


	});
   //Delete from cart
	$(document).on('click', '.dropdown-product-remove', function(e){
		e.preventDefault();
		product_id = $(this).data("product_id");
		console.log(product_id);
		qty = 0;
		//var url=form.attr("action");
		//var csrf_token = $('#csrf_hiden_code [name="csrfmiddlewaretoken"]').val();
		basketUpdate(product_id, qty, is_delete=true)

	});
  //update total amount in cart.html
	function calculateBasketAmount(){
		var total_order_amount = 0;
		$('.product-total-amount-in-basket').each(function(){
			total_order_amount += parseInt($(this).text());
			
			var product_total_amount_in_basket;
		});
		console.log(total_order_amount);
		$('#total_order_amount').text(total_order_amount);
	};

	$(document).on('change', ".quantity", function(){
		var current_num = $(this).val();
		var current_tr = $(this).closest('tr');
		var current_price = parseInt(current_tr.find('.product-in-basket-price').text());
		var total_amount = current_num*current_price;
 		current_tr.find('.product-total-amount-in-basket').text(total_amount);
 		calculateBasketAmount();
	})

	calculateBasketAmount();
	//Ajax фильтр по товару
	function getFilter(){
		var price = $('.slider-range-price')
		var minPrice = price.slider( "values", 0 );
		var maxPrice =  price.slider( "values", 1 );
		console.log(this)
		console.log(formFilter[0])
		var url = formFilter[0].action;
		var data = new URLSearchParams(new FormData(formFilter[0])).toString();
		console.log(url);
		console.log("&price="+minPrice+"&price="+maxPrice);
		console.log(maxPrice);
		console.log(data);
		var dataPage = "0"
		if(page>1) { dataPage=page}
		console.log(dataPage)
		$.get(url+"/?"+data+"&price="+minPrice+"&price="+maxPrice+"&page="+ dataPage+"&sort="+sortVal, function(data){
					console.log(data)
					console.log(data.products);
					const page = data.page
					const pages = data.pages
					$('.count-category').html("");
					$.each(data.brands, function(k, v){
						$('.count-category').append('\
						<div class="custom-control custom-checkbox d-flex align-items-center mb-2 control-checkbox">\
							<input type="checkbox" class="custom-control-input" id="customCheck'+v.id+'" name="brand" value="'+v.id+'" chacked="'+v.active+'" >\
							<label class="custom-control-label" for="customCheck'+v.id+'">'+v.name+' <span class="text-muted"> ('+v.count +')</span></label>\
						</div>');
						$('#customCheck'+v.id).prop('checked', v.active);
					});
					if(buttonGridList){
						$('.shop_list_product_area').addClass('shop_grid_product_area');
						$('.shop_grid_product_area').removeClass('shop_list_product_area');
						$('.row_grid_product_area').addClass('justify-content-center');
						$('.row_grid_product_area').html("");
						$('.shop_pagination_area').html("");	
						$.each(data.products, function(k, v){
							$('.row_grid_product_area').append('\
							<div class="col-9 col-sm-12 col-md-6 col-lg-4">\
								<div class="single-product-area mb-30">\
										<div class="product_image">\
												<!-- Product Image -->\
											<a href="/'+v.product__id+'/'+v.product__url+'">  \
												\
												<img class="normal_img" src="/media/'+v.image+'" alt="">\
												<img class="hover_img" src="" alt="">\
												\
											</a>'+(v.product__buyers_choice ? '<div class="product_badge"><span>TOP</span></div>':'')+'\
												\
												<!-- Wishlist -->\
												<div class="product_wishlist">\
														<a href="wishlist.html"><i class="fa fa-heart"></i></a>\
												</div>\
												<!-- Compare -->\
												<div class="product_compare">\
														<a href="compare.html"><i class="fa fa-exchange-alt" ></i></a>\
												</div>\
										</div>\
										<!-- Product Description -->\
										<div class="product_description">\
												<!-- Add to cart -->\
												<div class="product_add_to_cart">\
														<a href="#" class="btnCart" id="add_cart'+v.product__id+'" data-product_id= "'+v.product__id+'">\
														<i class="fa fa-shopping-cart"></i><b> В корзину</b> </a>\
												</div>\
												<!-- Quick View  product_quick_view -->\
												<div class="product_quick_view">\
														<a href="#" class="product_quickview" data-product_id="{{product.id}}" data-toggle="modal" data-target="#quickview">\
														<i class="fas fa-eye"></i><b> Просмотр</b></a>\
												</div>\
												<p>'+v.product__category__name+'</p>\
												<p>'+v.product__manufacturer__name+'</p>\
												<a href="/'+v.product__id+'/'+v.product__url+'"><i class="fa fa-arrows-h" ></i>'+v.product__name+'</a>\
												<div class="row d-flex justify-content-around align-items-center">\
												<h5 class="product-price"><b>'+v.product__price+' ₽</b></h5>\
												<div class="product_rating" id="star'+v.product__id+'">\
												</div>\
											</div>\
										</div>\
								</div>\
							</div>');
							id=v.product__id;
							rating=v.product__middlestar;
							(rating >= 1) ?  $('#star'+id).append('<i class="fa fa-star" aria-hidden="true"></i>') : $('#star'+id).append('<i class="far fa-star" aria-hidden="true"></i>');
							(rating >= 2) ?  $('#star'+id).append('<i class="fa fa-star" aria-hidden="true"></i>') : $('#star'+id).append('<i class="far fa-star" aria-hidden="true"></i>');
							(rating >= 3) ?  $('#star'+id).append('<i class="fa fa-star" aria-hidden="true"></i>') : $('#star'+id).append('<i class="far fa-star" aria-hidden="true"></i>');
							(rating >= 4) ?  $('#star'+id).append('<i class="fa fa-star" aria-hidden="true"></i>') : $('#star'+id).append('<i class="far fa-star" aria-hidden="true"></i>');
							(rating >= 5) ?  $('#star'+id).append('<i class="fa fa-star" aria-hidden="true"></i>') : $('#star'+id).append('<i class="far fa-star" aria-hidden="true"></i>');
							$('#star'+id).append('<span> '+v.product__countStar+'</span> ');
						});
					}else{
						$('.shop_grid_product_area').addClass('shop_list_product_area');
						$('.shop_list_product_area').removeClass('shop_grid_product_area');
						$('.row_grid_product_area').removeClass('justify-content-center');
						$('.row_grid_product_area').html("");
						$('.shop_pagination_area').html("");
						$.each(data.products, function(k, v){
							$('.row_grid_product_area').append('\
								<div class="col-12">\
	                                <div class="single-product-area mb-30">\
	                                    <div class="product_image">\
										  <a href="/'+v.product__id+'/'+v.product__url+'">  \
											<!-- Product Image -->\
	                                        <img class="normal_img" src="/media/'+v.image+'" alt="">\
											<img class="hover_img" src="img/product-img/best-5.png" alt="">\
										  </a>\
	                                        <div class="product_badge">\
	                                            <span>New</span>\
	                                        </div>\
	                                        <div class="product_wishlist">\
	                                            <a href="wishlist.html"><i class="icofont-heart"></i></a>\
	                                        </div>\
	                                        <div class="product_compare">\
	                                            <a href="compare.html"><i class="icofont-exchange"></i></a>\
	                                        </div>\
	                                    </div>\
	                                    <div class="product_description">\
	                                        <div class="product_add_to_cart">\
	                                            <a href="#" class="btnCart" id="add_cart'+v.product__id+'" data-product_id= "'+v.product__id+'"><i class="fa fa-shopping-cart"></i>  в Корзину</a>\
	                                        </div>\
	                                        <div class="product_quick_view">\
	                                            <a href="#" data-toggle="modal" data-target="#quickview"><i class="icofont-eye-alt"></i>Просмотр</a>\
	                                        </div>\
	                                        <p class="brand_name">Top</p>\
	                                        <a href="/'+v.product__id+'/'+v.product__url+'">'+v.product__name+'</a>\
	                                        <h5 class="product-price"><b>Цена: '+v.product__price+' ₽</b></h5>\
	                                        <p class="product-short-desc"> '+v.product__short_description+'</p>\
	                                    </div>\
	                                </div>\
	                             </div>');
						});	
					};
					$('.shop_pagination_area').append('\
					<nav aria-label="Page navigation">\
						<ul class="pagination pagination-sm justify-content-center">\
						</ul>\
					</nav>');
					for(var i=1; i<=pages; i++) {
						$('.pagination').append('\
								<li class="page-item pages'+i+'">\
                					<a class="page-link" href="#" id="page" data-page="'+i+'">'+ i +'</a>\
								</li>');
						
						if(i == page) $('.pages'+i).addClass('active');
					};
					window.scrollTo(0,0);
					
				});

	}
	//
	formFilter.on('submit', function(e){
		e.preventDefault();
		getFilter();
	});
	// Действия при нажатии на кнопку страница
	$(document).on('click', '#page', function(e){
		e.preventDefault();
		page = $(this).data("page");
		
		getFilter(page, sortVal);
	});

	sortBy.on('change', function(){
		
		sortVal = $(this).val()
		console.log('changeSort='+sortVal);
		getFilter(page, sortVal);
	})

	formFilter.on('change', function(e){
		e.preventDefault();
		console.log('change');
		var data1 = $('#customCheckAll input:checkbox:checked');
		var data =  $('#filter .control-checkbox input:checkbox:checked').length;
		

		(data) ? $('#customCheckAll').prop('checked', false) :  $('#customCheckAll').prop('checked', true);
		
	});

	formFilter.on('click','#customCheckAll', function(){
		//e.preventDefault();
		//if($(this).is(':checked'))
		$(this).prop('checked', true);
		$('.control-checkbox input:checkbox').prop('checked', false);
		
	});

	$(document).on('click', "#button-list", function(e){
		e.preventDefault();
		if(buttonGridList){
			$('#button-filter').trigger('click');
			//console.log("list");
			buttonGridList=0;
		}
	});
	
	$(document).on('click', "#button-grid", function(e){
		e.preventDefault();
		if(!buttonGridList){
			$('#button-filter').trigger('click');
			//console.log("list");
			buttonGridList=1;
		}
	});
	
	$('.btnCategory').click(function(e){
		e.preventDefault();
		var get_id = this.id;
		var get_current = $('.categoris .'+get_id);
		//console.log('.category .'+get_id);
		//$( '.category' ).scrollTop( 300 );
		 /*$('html, body').animate({
             scrollTop: get_current.offset().top
         }, 2000);*/
		//$('#'+get_id).get(0).scrollIntoView();
		$('.category').not(get_current).hide(500);
		get_current.show(500);
		
		setTimeout( function(){
			get_current.hide(500);
		    }, 5000 );
		
	});
	
	$('.btnCart').click(function(e){
		e.preventDefault();
		var product_name = $(this).data("product_name");
		var product_id = $(this).data("product_id");
		var qty= 1;
		$('#exampleModalLabel').html("");
		$('#exampleModalLabel').append(product_name+' добавлен в корзину.');
		var url = 'parent';
		$.get("../"+url+"/"+product_id+"/", function(data){
			$('.cart_slides').html("");
			$('#exampleModalHiader').html("");
			if(data.products.length)
				$('#exampleModalHiader').append('Вам так же может быть интересно');
			
			$.each(data.products, function(k, v){
				$('.cart_slides').append('\
					<div class="item">\
						<div class="single-product-area">\
							<div class="product_image">\
							<!-- Product Image -->\
							<a href="/'+v.product__id+'/'+v.product__url+'">  \
								<img class="normal_img" src="/media/'+v.image+'" alt=""> \
							</a>\
								<!-- Product Badge -->\
								<!--<div class="product_badge">\
										<span>TOP</span>\
								</div>-->\
							</div>\
							<h6 class="title">'+v.product__name+'</h6>\
						</div>\
			 		</div>'
				);
			});
			$('.cart_slides').owlCarousel({
				items: 3,
				margin: 20,
				loop: true,
				nav: true,
	
				navText: ['<i class="fa fa-arrow-circle-left"></i>', '<i class="fa fa-arrow-circle-right"></i>'],
				dots: false,
				autoplay: true,
				smartSpeed: 1500,
				autoplayTimeout: 7000,
				autoplayHoverPause: true,
				responsive: {
					0: {
						items: 3
					},
					480: {
						items: 3
					},
					768: {
						items: 3
					},
					992: {
						items: 3
					}
				}
			});
			
		});
		$("#basicExampleModal").modal();
		

		basketUpdate(product_id, qty, is_delete=false);
		
	});

	$('.product_quickview').click(function(e){
		e.preventDefault();
		var product_id = $(this).data("product_id");
		var url = 'quickview';
		$.get("../"+url+"/"+product_id+"/", function(data){
			
			$('.row_quickview').html("");
			$.each(data.product, function(k, v){
				$('.row_quickview').append('\
				<div class="col-12 col-lg-5">\
					<div class="quickview_pro_img m-2">\
						<img class="first_img" src="/media/'+v.image+'" alt="">\
						\
						<!-- Product Badge -->\
						<div class="product_badge">\
							<span class="badge-new">New</span>\
						</div>\
					</div>\
				</div>\
				<div class="col-12 col-lg-7">\
					<div class="quickview_pro_des">\
						<h4 class="title">'+v.product__name+'</h4>\
						<div class="top_seller_product_rating mb-15">\
							<i class="fa fa-star" aria-hidden="true"></i>\
							<i class="fa fa-star" aria-hidden="true"></i>\
							<i class="fa fa-star" aria-hidden="true"></i>\
							<i class="fa fa-star" aria-hidden="true"></i>\
							<i class="fa fa-star" aria-hidden="true"></i>\
						</div>\
						<h5 class="price"><b>Цена: '+v.product__price+' ₽</b></h5>\
						<p>'+v.product__short_description+'</p>\
						<a href="/'+v.product__id+'/'+v.product__url+'">Посмотреть полное описание</a>\
					</div>\
					<!-- Add to Cart Form -->\
					<form class="cart"  id="form_bay_prod_datail" action="/basket_adding/">\
						<div class="quantity">\
							<input type="number" class="qty-text form-control" id="qty2" step="1" min="1" max="'+v.product__rest+'" name="quantity" value="1">\
						</div>\
						<button type="submit" name="addtocart" value="5" id="btn_submit"\
						 class="btn btn-danger mt-1 mt-md-0 ml-1 ml-md-3"\
						 data-product_id= "'+v.product__id+'"\
						 data-product_name= "'+v.product__name+'"\
						 data-product_price= "'+v.product__price+'"\
						 data-product_url="/media/'+v.image+'">\
						 Добавить в корзину</button>\
						<!-- Wishlist -->\
						<div class="modal_pro_wishlist">\
							<a href="wishlist.html"><i class="icofont-heart"></i></a>\
						</div>\
						<!-- Compare -->\
						<div class="modal_pro_compare">\
							<a href="compare.html"><i class="icofont-exchange"></i></a>\
						</div>\
					</form>\
					<!-- Share -->\
					<div class="share_wf mt-30">\
						<p>Поделиться с друзьями</p>\
						<div class="_icon">\
							<a href="#"><i class="fab fa-facebook" aria-hidden="true"></i></a>\
							<a href="#"><i class="fab fa-twitter" aria-hidden="true"></i></a>\
							<a href="#"><i class="fab fa-pinterest" aria-hidden="true"></i></a>\
							<a href="#"><i class="fab fa-linkedin" aria-hidden="true"></i></a>\
							<a href="#"><i class="fab fa-instagram" aria-hidden="true"></i></a>\
							<a href="#"><i class="fab fa-envelope-o" aria-hidden="true"></i></a>\
						</div>\
					</div>\
				</div>');
			});
		});
		

	});
});
