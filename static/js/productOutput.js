var selectedStorage = $('select#id_storage').val();
function switchStorage (storage) {
	switch (storage){
		case "C":
			$('select#id_product_consignment').closest('.form-group').show();
			$('select#id_product_stock').closest('.form-group').hide();
			$('select#id_product_used').closest('.form-group').hide();
			selectedStorage = storage;
			break;
		case "S":
			$('select#id_product_consignment').closest('.form-group').hide();
			$('select#id_product_stock').closest('.form-group').show();
			$('select#id_product_used').closest('.form-group').hide();
			selectedStorage = storage;
			break;
		case "U":
			$('select#id_product_consignment').closest('.form-group').hide();
			$('select#id_product_stock').closest('.form-group').hide();
			$('select#id_product_used').closest('.form-group').show();
			selectedStorage = storage;
			break;
		default:
			$('select#id_product_consignment').closest('.form-group').hide();
			$('select#id_product_stock').closest('.form-group').hide();
			$('select#id_product_used').closest('.form-group').hide();
			selectedStorage = storage;
			break;
	}
}
switchStorage($('select#id_storage').val());
$('select#id_storage').change(function () {
	switchStorage($(this).val());
});

var $outputProductsSelect = $('#outputProducts');
$('#addOutputProduct').click(function (argument) {
	var amount = $('#id_amount').val() || "1"
	var selectedProducts = []
	switch (selectedStorage){
		case "C":
			selectedProducts = $('#id_product_consignment option:selected');
			break;
		case "S":
			selectedProducts = $('#id_product_stock option:selected');
			break;
		case "U":
			selectedProducts = $('#id_product_used option:selected');
			break;
		default:
			break;
	}
	if (selectedProducts.length){
		selectedProducts.each(function(){
			if(!$outputProductsSelect.find("option[value^='"+$(this).val()+"']").length){
	            $outputProductsSelect.append($('<option>', {
	                value:$(this).val()+":"+amount,
	                text:$(this).text()+ " x "+amount
	            }));
	            $('select#id_storage').attr('disabled', true);
	        }
	        else{
	            showNotification("Producto ya agregado", "info");
	        }
		})
	}
	else {
		showNotification("No se ha seleccionado un producto", "info");
	}
	return false;
});

$('#removeOutputProduct').click(function (argument) {
    $outputProductsSelect.find('option:selected').remove();
    if ($outputProductsSelect.children().length == 0){
    	$('select#id_storage').removeAttr('disabled');
    }
    return false;
});

$('#new_output form').submit(function () {
	$('select#id_storage').removeAttr('disabled');
	var productList = {};
	$outputProductsSelect.find('option').each(function(){
		productList[$(this).val().split(":")[0]] = $(this).val().split(":")[1];
	});
	$('#new_output form input[name="outputProducts"]').val(JSON.stringify(productList));
});

$('form#multi-delete').submit(function () {
	var outputList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			outputList.push($(this).val())
		}
	})
	$('form#multi-delete input[name="rollback"]').val($('form#multi-delete input#rollback')[0].checked)
	$('form#multi-delete input[name="output_id"]').val(JSON.stringify(outputList));
});

$('form#single-delete').submit(function () {
	$(this).find('input[name="rollback"]').val($(this).find('input#rollback')[0].checked)
});

var filterSearch = $('#id_filter_search');
filterSearch.keyup(function() {
	if ($(this).val() !== ""){
		$('#id_product_consignment option').each(function() {
            var regex = new RegExp(filterSearch.val(),"gi");
            if($(this).text().match(regex) !== null){
                $(this).prependTo($('#id_product_consignment'));
            }
		});
		$('#id_product_stock option').each(function() {
            var regex = new RegExp(filterSearch.val(),"gi");
            if($(this).text().match(regex) !== null){
                $(this).prependTo($('#id_product_stock'));
            }
		});
		$('#id_product_used option').each(function() {
            var regex = new RegExp(filterSearch.val(),"gi");
            if($(this).text().match(regex) !== null){
                $(this).prependTo($('#id_product_used'));
            }
		});
	}
});
var filterProvider = $('#id_provider');
filterProvider.change(function (argument) {
	$('#id_product_consignment option').each(function() {
		$(this).show();
	});
	$('#id_product_stock option').each(function() {
		$(this).show();
	});
	$('#id_product_used option').each(function() {
		$(this).show();
	});
	if ($(this).val() !== ""){
		$('#id_product_consignment option').each(function() {
            if ($(this).attr("provider") != filterProvider.val()){
				$(this).hide();
            }
		});
		$('#id_product_stock option').each(function() {
            if ($(this).attr("provider") != filterProvider.val()){
				$(this).hide();
            }
		});
		$('#id_product_used option').each(function() {
            if ($(this).attr("provider") != filterProvider.val()){
				$(this).hide();
            }
		});
	}
});