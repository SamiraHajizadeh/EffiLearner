
def remove_whitespaces(input_string: str) -> str:
    return str.replace(input_string, ' ', '')

print(remove_whitespaces(' Google    Flutter '))
print(remove_whitespaces('  Google    Dart  '))
print(remove_whitespaces('  iOSSwift  '))
assert remove_whitespaces(' Google    Flutter ') == 'GoogleFlutter'
assert remove_whitespaces(' Google    Dart ') == 'GoogleDart'
assert remove_whitespaces(' iOS    Swift ') == 'iOSSwift'