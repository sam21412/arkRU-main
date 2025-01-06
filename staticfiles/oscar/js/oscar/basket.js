var oscar = oscar || {};

oscar.basket = {
    init: function(options) {
        // ...existing code...
        
        // Add handler for option changes
        $(document).on('change', '.option-select', function() {
            var optionId = $(this).val();
            var lineId = $(this).data('line-id');
            
            $.ajax({
                url: '/catalogue/option-price/',
                data: {
                    option_id: optionId
                },
                success: function(data) {
                    oscar.basket.updateLinePrice(lineId, data.price);
                }
            });
        });
    },

    updateLinePrice: function(lineId, optionPrice) {
        var $line = $('#line_' + lineId);
        var basePrice = parseFloat($line.data('base-price'));
        var newPrice = basePrice + optionPrice;
        
        $line.find('.line-price').text(oscar.currency.format(newPrice));
        
        // Trigger basket refresh
        oscar.basket.refreshContent();
    }
};
