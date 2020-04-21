//
//  InputField.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import Foundation

// Useful protocol that allows to store and force validation of all required fields on account view 
protocol InputField {
    @discardableResult
    func forceValidation() -> Bool
}
