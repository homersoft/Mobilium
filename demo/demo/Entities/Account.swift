//
//  Account.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Grzegorz Przybyła. All rights reserved.
//

import Foundation

struct Account: Equatable {
    let firstName: String
    let lastName: String
    let phoneNumber: String
    let email: String
    let location: String
    let picture: Data

    init(firstName: String, lastName: String, phoneNumber: String,
         email: String, location: String, picture: Data) {
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.email = email
        self.location = location
        self.picture = picture
    }

    init(from account: AccountDBO) {
        self.firstName = account.firstName
        self.lastName = account.lastName
        self.phoneNumber = account.phoneNumber
        self.email = account.email
        self.location = account.location
        self.picture = account.picture
    }

    func toDBO() -> AccountDBO {
        AccountDBO(firstName: firstName,
                   lastName: lastName,
                   phoneNumber: phoneNumber,
                   email: email,
                   location: location,
                   picture: picture)
    }
}
