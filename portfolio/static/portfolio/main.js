function openModal(id) {
    document.getElementById(id).showModal();
}

function closeModal(id) {
    document.getElementById(id).close();
}

function openEditAssetModal(btn) {
    document.getElementById('editAssetForm').action = btn.dataset.url;
    document.getElementById('edit_asset_name').value = btn.dataset.name;
    document.getElementById('edit_asset_ticker').value = btn.dataset.ticker;
    document.getElementById('edit_asset_quantity').value = btn.dataset.quantity.replace(',', '.');
    document.getElementById('edit_asset_price').value = btn.dataset.price.replace(',', '.');

    const deleteForm = document.getElementById('deleteAssetForm');
    deleteForm.action = btn.dataset.deleteUrl;
    deleteForm.onsubmit = function () {
        return confirm('Delete ' + btn.dataset.name + '?');
    };

    openModal('editAssetModal');
}

document.addEventListener('DOMContentLoaded', function () {
    const modalToOpen = document.querySelector('dialog[data-auto-open="true"]');
    if (modalToOpen) {
        modalToOpen.showModal();
    }
});