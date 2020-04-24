//
//  XCUIApplication.swift
//  MobiliumDriver
//
//  Created by Mateusz Mularski on 12/09/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import XCTest

extension XCUIApplication {
    func element(with accessibilityId: String, index: Int) -> XCUIElement {
        return descendants(matching: .any).matching(identifier: accessibilityId).element(boundBy: index)
    }
}
