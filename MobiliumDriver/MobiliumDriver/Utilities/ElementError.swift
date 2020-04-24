//
//  ElementError.swift
//  MobiliumDriver
//
//  Created by Grzegorz Przybyła on 18/09/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import Foundation

extension ElementError {
    static let elementNotExists: ElementError = {
        var error = ElementError()
        error.reason = .elementNotExists(ElementNotExists())
        return error
    }()
}
