//
//  XPathParserTests.swift
//  MobiliumDriverTests
//
//  Created by Tomasz Oraczewski on 06/11/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

@testable import MobiliumFramework
import XCTest

class XPathParserTests: XCTestCase {

    func testParseEmptyXPath() {
        let result = XPathParser.parse("")

        XCTAssertTrue(result.isEmpty)
    }
}
