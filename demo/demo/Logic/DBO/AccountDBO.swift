//
//  AccountDBO.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import Foundation

struct AccountDBO: Codable {
    let firstName: String
    let lastName: String
    let phoneNumber: String
    let email: String
    let location: String
    let picture: Data
}
