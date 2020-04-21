//
//  KeyPathBuildable.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import UIKit

protocol KeyPathBuildable {}

extension KeyPathBuildable {
    func set<T>(_ keyPath: WritableKeyPath<Self, T>, to newValue: T) -> Self {
        var copy = self
        copy[keyPath: keyPath] = newValue
        return copy
    }
}

extension UIView: KeyPathBuildable {}
extension UIViewController: KeyPathBuildable {}
