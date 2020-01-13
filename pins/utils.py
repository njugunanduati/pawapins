import random
import string
import logging


from pins.models import CardPreview


def generate_pins(length, count):
    """
    http://stackoverflow.com/a/1436574/1690654

    """
    alphabet=string.digits
    alphabet = ''.join(set(alphabet))
    if count > len(alphabet)**length:
      raise ValueError("error:Can't generate more than %s > %s pins of length %d out of %r"% (count,
                     len(alphabet)**length, length, alphabet))
    def onepin(length):
        pin = ''.join(random.choice(alphabet) for x in range(length))
        if pin.startswith('0'):
            return onepin(length)
        return pin
    result = set(onepin(length) for x in range(count))
    return list(result)


def generate_cards(totalcards, card_batch):
    pins_generated = 0
    try:
        print("generating cards:{}".format(card_batch.id))
        pins = generate_pins(16, totalcards+200)
        for pin in pins:
            if pins_generated >= totalcards:
                break
            if not CardPreview.objects.filter(pin=pin).exists():
                card_preview = CardPreview(
                    pin=pin, batch=card_batch, printed=0)
                card_preview.save()
                pins_generated += 1
        if pins_generated < totalcards:
            generate_cards(totalcards-pins_generated, card_batch)
    except Exception as e:
        print("generate_cards:fail;card_batch:%s;" % (str(card_batch)))
        logging.exception(e)
        card_batch.status = 1
        card_batch.save()
    else:
        card_batch.status = 2
        card_batch.save()
        print("generate_cards:success;card_batch:%s;cardsgenerated:%s;" % (str(card_batch),
                                                                           str(pins_generated)))
