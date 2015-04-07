$('.product-input').each(function () {
	$(this).find(".discount").keyup(function () {
		calculateRealPrice($(this).closest(".product-input"));
	});
	$(this).find(".discount").change(function () {
		calculateRealPrice($(this).closest(".product-input"));
	});
	$(this).find(".price").keyup(function () {
		calculateRealPrice($(this).closest(".product-input"));
	});
	$(this).find(".price").change(function () {
		calculateRealPrice($(this).closest(".product-input"));
	});
});

function calculateRealPrice (section) {
	var discount = section.find(".discount").val();
	var price = section.find('.price').val();
	section.find('.real_price').val((price-price*discount/100).toFixed(2));
}

$(document).on('click', '.unlist-product', function (){
	$(this).closest(".form-group").remove();
});