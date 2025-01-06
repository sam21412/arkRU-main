$(document).ready(function() {
    // Обработчик изменения атрибута
    $('.attribute-option-select').on('change', function() {
        var optionId = $(this).val();
        var $form = $(this).closest('form');
        var $priceElement = $form.find('.price_color');
        var basePrice = parseFloat($form.data('base-price'));

        // Получаем цену атрибута через AJAX
        $.get('/catalogue/get-attribute-price/', {
            option_id: optionId
        })
        .done(function(data) {
            if (data.status === 'success') {
                // Обновляем цену с учетом атрибута
                var newPrice = basePrice + data.price;
                $priceElement.text(oscar.currency.format(newPrice));
            }
        });
    });
});
