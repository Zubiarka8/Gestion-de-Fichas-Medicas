        document.addEventListener('DOMContentLoaded', function() {
            new TomSelect('#select-area', {
                create: false,
                sortField: {
                    field: "text",
                    direction: "asc"
                }
            });
        });