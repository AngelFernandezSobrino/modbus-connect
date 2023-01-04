# Test gateway core methods

# Import gateway module

import src.modbus_connect.utils as utils


# Test the get_batch_memory_length function

def test_get_batch_memory_length():

    batch = [
        utils.ObjectWithAddressAndBank(0, 'bank1', 1),
        utils.ObjectWithAddressAndBank(1, 'bank1', 1),
        utils.ObjectWithAddressAndBank(2, 'bank1', 1),
        utils.ObjectWithAddressAndBank(3, 'bank1', 1),
        utils.ObjectWithAddressAndBank(4, 'bank1', 1),
    ]

    assert utils.get_batch_memory_length(batch) == 5

# Test the make_batch_consecutive_bank_and_size function

def test_make_batch_consecutive_bank_and_size():
    
    # Create a list with some example ObjectWithAddressAndBank objects
    tags_list = [
        utils.ObjectWithAddressAndBank(0, 'bank1', 1),
        utils.ObjectWithAddressAndBank(1, 'bank1', 1),
        utils.ObjectWithAddressAndBank(2, 'bank1', 1),
        utils.ObjectWithAddressAndBank(3, 'bank1', 1),
        utils.ObjectWithAddressAndBank(4, 'bank1', 1),
        utils.ObjectWithAddressAndBank(5, 'bank1', 1),
        utils.ObjectWithAddressAndBank(10, 'bank1', 1),
        utils.ObjectWithAddressAndBank(11, 'bank1', 1),
        utils.ObjectWithAddressAndBank(12, 'bank1', 1),
        utils.ObjectWithAddressAndBank(13, 'bank1', 1),
        utils.ObjectWithAddressAndBank(14, 'bank1', 2),
        utils.ObjectWithAddressAndBank(16, 'bank1', 2),
        utils.ObjectWithAddressAndBank(18, 'bank1', 2),
        utils.ObjectWithAddressAndBank(20, 'bank1', 2),
        utils.ObjectWithAddressAndBank(22, 'bank1', 2),
        utils.ObjectWithAddressAndBank(24, 'bank2', 1),
        utils.ObjectWithAddressAndBank(25, 'bank2', 1),
        utils.ObjectWithAddressAndBank(26, 'bank2', 1),
        utils.ObjectWithAddressAndBank(27, 'bank2', 1),
        utils.ObjectWithAddressAndBank(28, 'bank2', 1),
        utils.ObjectWithAddressAndBank(29, 'bank2', 1),
    ]

    # Make batches

    batches = utils.make_batch_consecutive_bank_and_size(tags_list, 5)

    # Check batches

    assert len(batches) == 6
    assert len(batches[0]) == 5

