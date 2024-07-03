from password_generator import Generator

from cvback.events.models import APIToken


def api_key_generator(n_generated=12, top_selected=8):
    generator = Generator()
    generator.generator(n_generated, 32)  # Generate 12 password suggestions of length 32
    top_passwords = generator.get_top_passwords(top_selected)  # Retrieve the top 5 password suggestions
    for password in top_passwords:
        existing_keys = APIToken.objects.filter(key=password['suggested password'])
        if existing_keys.len() == 0:
            return password['suggested password']
    else:
        raise Exception(f'All of the {top_selected} top passwords where existing API keys!')
