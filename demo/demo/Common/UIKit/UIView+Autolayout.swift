//
//  UIView+Autolayout.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import UIKit

extension UIView {
    static func makeForAutolayout() -> Self {
        let view = Self.init()
        view.translatesAutoresizingMaskIntoConstraints = false
        return view
    }
}
