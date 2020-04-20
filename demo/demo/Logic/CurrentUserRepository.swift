//
//  CurrentUserRepository.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Grzegorz Przybyła. All rights reserved.
//

import Foundation

private enum Key: String {
    case userId
    case phoneNumber
}

class CurrentUserRepository {
    let userDefault: UserDefaults

    init(userDefault: UserDefaults = .standard) {
        self.userDefault = userDefault
    }

    func getCurrentUser() -> User? {
        guard let userId = userDefault.string(forKey: Key.userId.rawValue) else {
            return nil
        }

        return User(identifier: userId, phoneNumber: userDefault.string(forKey: Key.phoneNumber.rawValue))
    }

    func store(user: User) {
        userDefault.set(user.identifier, forKey: Key.userId.rawValue)
        userDefault.set(user.phoneNumber, forKey: Key.phoneNumber.rawValue)
    }

    func clear() {
        userDefault.removeObject(forKey: Key.userId.rawValue)
        userDefault.removeObject(forKey: Key.phoneNumber.rawValue)
    }
}
