//
//  CombineCompatible.swift
//  demo
//
//  Source https://www.avanderlee.com/swift/custom-combine-publisher/
//

import UIKit
import Combine

protocol CombineCompatible { }
extension UIControl: CombineCompatible { }

extension CombineCompatible where Self: UIControl {
    func publisher(for events: UIControl.Event) -> UIControlPublisher<Self> {
        return UIControlPublisher(control: self, events: events)
    }
}
