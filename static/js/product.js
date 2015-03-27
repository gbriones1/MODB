$('button[data-target="#new_input"]').click(function () {
	var productList = getSelectedProducts();
	if (productList.length){
		var $formBody = $('#new_input .modal-body .fields-area');
		$formBody.empty();
		for (var productIdx in productList){
			var fieldStr = '<div class="form-group"><label class="col-sm-8 control-label">';
			fieldStr += getProductName(productList[productIdx]);
			fieldStr += '</label><div class="col-sm-4">';
			fieldStr += '<input type="number" class="form-control" name="'+productList[productIdx]+'" value="1" />';
			fieldStr += '</div></div>';
			$formBody.append(fieldStr);
		}
	}
	else{
		showNotification('Debes seleccionar al menos un producto', 'info')
	}
});

$('#new_input form').submit(function () {
	var inputProducts = {};
	$('#new_input form .modal-body input').each(function () {
		inputProducts[$(this).attr("name")] = $(this).val();
	});
	$('#new_input form input[name="inputProducts"]').val(JSON.stringify(inputProducts));
});

$('button[data-target="#new_output"]').click(function () {
	var productList = getSelectedProducts();
	if (productList.length){
		var $formBody = $('#new_output .modal-body .fields-area');
		$formBody.empty();
		for (var productIdx in productList){
			var fieldStr = '<div class="form-group"><label class="col-sm-8 control-label">';
			fieldStr += getProductName(productList[productIdx]);
			fieldStr += '</label><div class="col-sm-4">';
			fieldStr += '<input type="number" class="form-control" name="'+productList[productIdx]+'" value="1" />';
			fieldStr += '</div></div>';
			$formBody.append(fieldStr);
		}
	}
	else{
		showNotification('Debes seleccionar al menos un producto', 'info')
	}
});

$('#new_output form').submit(function () {
	var outputProducts = {};
	$('#new_output form .modal-body input').each(function () {
		outputProducts[$(this).attr("name")] = $(this).val();
	});
	$('#new_output form input[name="outputProducts"]').val(JSON.stringify(outputProducts));
});

$('button[data-target="#new_lending"]').click(function () {
	var productList = getSelectedProducts();
	if (productList.length){
		var $formBody = $('#new_lending .modal-body');
		$formBody.empty();
		for (var productIdx in productList){
			var fieldStr = '<div class="form-group"><label class="col-sm-8 control-label">';
			fieldStr += getProductName(productList[productIdx]);
			fieldStr += '</label><div class="col-sm-4">';
			fieldStr += '<input type="number" class="form-control" name="'+productList[productIdx]+'" value="1" />';
			fieldStr += '</div></div>';
			$formBody.append(fieldStr);
		}
	}
	else{
		showNotification('Debes seleccionar al menos un producto', 'info')
	}
});

$('form#multi-delete').submit(function () {
	var productList = getSelectedProducts();
	if (productList.length){
		$('form#multi-delete input[name="code"]').val(JSON.stringify(productList));
	}
	else{
		showNotification('Debes seleccionar al menos un producto', 'info');
		return false;
	}
});

$('input[name="storage"]').each(function () {
	var storage = $(this).val();
	switch (storage){
		case "C":
			$(this).closest('form').find('[name="in_stock"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="stock_tobe"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="in_used"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="used_tobe"]').closest(".form-group").hide()
			break;
		case "S":
			$(this).closest('form').find('[name="in_consignment"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="consignment_tobe"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="in_used"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="used_tobe"]').closest(".form-group").hide()
			break;
		case "U":
			$(this).closest('form').find('[name="in_stock"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="stock_tobe"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="in_consignment"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="consignment_tobe"]').closest(".form-group").hide()
			break;
	}
});

function getProductName (code) {
	return $('tr#'+code+' td.product-name').text()
}

function getSelectedProducts () {
	var productList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			productList.push($(this).val())
		}
	});
	return productList;
}

function filterProducts (field, query) {
	$('table tbody tr').each(function(){
		value = $(this).attr('data-'+field);
		if (value.indexOf(query)+1){
			$(this).show();
		}
		else{
			$(this).hide();
		}
	});
}

$(".input-filter").keyup(function () {
	filterProducts($(this).attr("data-field"), $(this).val());
});

$(".select-filter").change(function () {
	filterProducts($(this).attr("data-field"), $(this).val());
});

$(document).on('click', 'button.edit-modal', function () {
    $('.edit-iframe').attr('data-id', $(this).attr('data-id'));
    $('.edit-iframe').attr('src', '/product/'+$(this).attr('data-id')+'/?storage='+$('#new input[name="storage"]').val());
});

$(document).on('click', '#edit button[type="submit"]', function (argument) {
	var form = $('.edit-iframe').contents().find('form').clone();
	form.hide();
	form.appendTo($('body'));
	form.submit();
});

$('.edit-iframe').load(function () {
	switch ($('#new input[name="storage"]').val()){
		case "C":
			$(this).contents().find('[name="in_stock"]').closest(".form-group").hide()
			$(this).contents().find('[name="stock_tobe"]').closest(".form-group").hide()
			$(this).contents().find('[name="in_used"]').closest(".form-group").hide()
			$(this).contents().find('[name="used_tobe"]').closest(".form-group").hide()
			break;
		case "S":
			$(this).contents().find('[name="in_consignment"]').closest(".form-group").hide()
			$(this).contents().find('[name="consignment_tobe"]').closest(".form-group").hide()
			$(this).contents().find('[name="in_used"]').closest(".form-group").hide()
			$(this).contents().find('[name="used_tobe"]').closest(".form-group").hide()
			break;
		case "U":
			$(this).contents().find('[name="in_stock"]').closest(".form-group").hide()
			$(this).contents().find('[name="stock_tobe"]').closest(".form-group").hide()
			$(this).contents().find('[name="in_consignment"]').closest(".form-group").hide()
			$(this).contents().find('[name="consignment_tobe"]').closest(".form-group").hide()
			break;
	}
	$('#edit').on('shown.bs.modal', function (e) {
		$('.edit-iframe').height($('.edit-iframe').contents().find('html').height());
	});
	$('.edit-iframe').height($('.edit-iframe').contents().find('html').height());
});

$(document).on('click', 'button.delete-modal', function () {
    $('#single-delete input[name="code"]').val('["'+$(this).attr('data-id')+'""]');
});