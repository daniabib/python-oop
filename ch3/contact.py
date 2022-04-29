from __future__ import annotations
from typing import Any, Optional, Protocol


class AdressHolder:
    def __init__(self, street: str, city: str, state: str, code: str) -> None:
        self.street = street
        self.city = city
        self.state = state
        self.code = code


class ContactList(list['Contact']):
    def search(self, name: str) -> list[Contact]:
        matching_contacts: list[Contact] = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts


class Contact:
    all_contacts = ContactList()

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        Contact.all_contacts.append(self)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.email!r}"
            f")"
        )


class Suplier(Contact):
    def order(self, order: Order) -> None:
        print(
            "If this were a real system we would send "
            f"'{order}' order to '{self.name}'"
        )


class Friend(Contact, AdressHolder):
    def __init__(self, name: str, email: str, phone: str) -> None:
        super().__init__(name, email)
        self.phone = phone


class LongNameDict(dict[str, int]):
    def longest_key(self) -> Optional[str]:
        """In effect, max(self, key=len), but less obscure"""
        longest = None
        for key in self:
            if longest is None or len(key) > len(longest):
                longest = key
        return longest


class Emailable(Protocol):
    email: str


class MailSender(Emailable):
    def send_mail(self, message: str) -> None:
        print(f"Sending mail to {self.email}")
        # Add e-mail logic here


class EmaiableContact(Contact, MailSender):
    ...


class Order:
    ...


orders: list[Any] = []

if __name__ == "__main__":
    c1 = Contact("Nico", "nico.com")
    print(c1)