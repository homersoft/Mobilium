//
//  XCUIApplication.swift
//  MobiliumDriver
//
//  Created by Mateusz Mularski on 12/09/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import XCTest

extension XCUIApplication {
    func element(with accessibilityId: String) -> XCUIElement {
        return descendants(matching: .any)[accessibilityId].firstMatch
    }
}
